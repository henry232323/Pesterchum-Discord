#!/usr/bin/env python
from playsound import playsound  # Modified version, original tries to join a list of strs and bytes, decodes the bytes
from options import Options
import subprocess
import requests
import sys

__version__ = "v1.2.0"
__author__ = "henry232323"

if Options["interface"]["auto_update"]:
    response = requests.get("https://api.github.com/repos/henry232323/pesterchum-discord/releases/latest").json()
    current_version = response["tag_name"]
    if current_version > __version__:
        playsound("resources/update.wav", block=False)
        download_url = response["assets"][0]["browser_download_url"]
        subprocess.call("start updater.exe {}".format(download_url), shell=True)
        sys.exit()

from quamash import QEventLoop, QThreadExecutor
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QColor

from inspect import isawaitable
import discord
import asyncio
import os.path

from dialogs import AuthDialog, ConnectingDialog
from themes import themes, getThemes
from auth import UserAuth, save_auth
from formatting import fmt_disp_msg
from options import save_options
from client import DiscordClient
from mentions import Mentions
from emojis import Emojis
from quirks import Quirks
from moods import Moods
from gui import Gui


class App(QApplication):
    def __init__(self):
        QApplication.__init__(self, sys.argv)
        # Establish loop as Quamash Event Loop
        loop = QEventLoop(self)
        self.loop = loop
        asyncio.set_event_loop(loop)

        self.idle = False
        self.trayIcon = None

        self.themes = themes
        self.options = Options
        try:
            self.theme = themes[self.options["theme"]["theme"]]
        except KeyError:
            self.theme = themes["Pesterchum 2.5"]
        self.theme_name = self.theme["name"]
        self.moods = Moods
        self.emojis = Emojis
        self.mentions = Mentions
        self.setStyleSheet(self.theme["styles"])

        self.nick = None
        self.client = DiscordClient(app=self, loop=self.loop)

        self.user, self.passwd, self.token, self.botAccount = UserAuth

        if not UserAuth[0] and not UserAuth[1] and not UserAuth[2]:
            self.openAuth(i=True)
            save_auth((self.user, self.passwd, self.token, self.botAccount,))

        asyncio.ensure_future(self.connecting())
        asyncio.ensure_future(self.runbot())
        self.gui = Gui(self.loop, self)
        loop.run_forever()

    def cli(self):
        """
        Runs a REPL style loop, if eval(input) is awaitable (`inspect.isawaitable`)
        will await, runs in an executor
        """
        asyncio.ensure_future(self.run_exe())

    async def run_exe(self):
        while True:
            try:
                with QThreadExecutor(1) as exec:
                    line = await self.loop.run_in_executor(exec, input, ">>> ")
                evl = eval(line)
                if isawaitable(evl):
                    r = await evl
                    print(r)
                else:
                    print(evl)
            except Exception as e:
                print(e)

    async def connecting(self):
        self.connectingDialog = ConnectingDialog(self, self)
        self.connectingDialog.exec_()

    async def on_message(self, message):
        """Called on `Client.on_message`, Message handling happens here"""
        if message.content.startswith("_") and message.content.endswith("_"):
            message.content = "/me " + message.content[1:-1]
        if isinstance(message.channel, discord.PrivateChannel):
            if not message.channel.name:
                message.channel.name = ",".join(map(lambda m: m.display_name, message.channel.recipients))
            if message.channel.type is discord.ChannelType.group:
                tab = self.gui.start_privmsg(message.channel)
            else:
                tab = self.gui.start_privmsg(message.channel)
            fmt = fmt_disp_msg(self, message.content, message, user=message.author)
            if fmt:
                tab.display_text(fmt)
        else:
            if self.gui.memosWindow:
                if message.server in self.gui.memosWindow.open.keys():
                    fmt = fmt_disp_msg(self, message.content, message, user=message.author)
                    if fmt:
                        try:
                            self.gui.memosWindow.display_message(message.channel, fmt)
                        except AttributeError as e:
                            print(e)

    async def on_ready(self):
        """Called on `Client.on_ready`, generally once the client is logged in and ready"""
        self.connectingDialog.close()
        self.nick = self.client.user.name
        self.quirks = Quirks(self)
        if "debug" in sys.argv:
            self.cli()
        playsound(os.path.join(self.theme["path"], "alarm.wav"), block=False)
        self.gui.initialize()

    def change_mood(self, mood):
        if mood == "offline" or mood == "abscond":
            asyncio.ensure_future(self.client.change_presence(status=discord.Status.invisible))
        else:
            asyncio.ensure_future(self.client.change_presence(game=discord.Game(name="Feeling {}".format(mood.upper())), status=discord.Status.online))

        if self.idle:
            self.gui.toggleIdle()

    def change_theme(self, theme, f=False):
        if f:
            self.refresh_themes()
        if theme != self.theme_name or f:
            self.theme = themes[theme]
            self.theme_name = self.theme["name"]
            self.setStyleSheet(self.theme["styles"])
            if hasattr(self, "gui"):
                self.gui.close()
                self.gui = Gui(self.loop, self)
                self.gui.initialize()

    def refresh_themes(self):
        self.themes = getThemes(dict())

    @staticmethod
    def getColor(member, type=str):
        """Get the given primary role color for a `Member`, returns a `Discord.Color` instance"""
        try:
            clr = member.color
        except AttributeError:
            clr = discord.Color.default()
        if type is str:
            return "rgb({clr.r},{clr.g},{clr.b})".format(clr=clr)
        elif type is QColor:
            return QColor(clr.r, clr.g, clr.b)

    def send_msg(self, message, channel):
        """Send message `message` to the User, Private Channel, or Channel `channel`"""
        message = message.strip()
        tts = False
        if message.startswith("/me"):
            message = "_" + message[3:] + "_"
        if message.startswith("/tts "):
            message = message[4:]
            tts = True
        if message.startswith("/ooc"):
            message = "((" + message[4:] + "))"
        message = self.quirks.process_quirks(message)
        asyncio.ensure_future(self.client.send_message(channel, message, tts=tts))

    def openAuth(self, f=False, i=True):
        auth = AuthDialog(self, self, f=f, i=i).auth
        self.user, self.passwd, self.token, self.botAccount = auth
        if hasattr(self, "gui") and auth and not f:
            self.exit()

    async def runbot(self):
        try:
            if (self.user and self.passwd) and not self.token:
                await self.client.start(self.user, self.passwd, bot=False)
            elif self.token and not (self.user or self.passwd):
                await self.client.start(self.token, bot=self.botAccount)
        except discord.LoginFailure:
            self.openAuth(f=True)
            save_auth((self.user, self.passwd, self.token, self.botAccount,))
        finally:
            await self.runbot()

    def exit(self, code=0):
        """
        Called when exiting the client
        Save configurations and sys.exit
        """
        try:
            save_auth((self.user, self.passwd, self.token, self.botAccount,))
            save_options(self.options)
            self.quirks.save_quirks()
        except:
            pass
        finally:
            sys.exit(code)

    def lastWindowClosed(self):
        self.exit()

App()
