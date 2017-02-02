#!/usr/bin/env python
import subprocess
import requests
import sys
from options import Options

__version__ = "v1.0.5"

if Options["interface"]["auto_update"]:
    response = requests.get("https://api.github.com/repos/henry232323/pesterchum-discord/releases/latest").json()
    current_version = response["tag_name"]
    if current_version > __version__:
        download_url = response["assets"][0]["browser_download_url"]
        subprocess.call("start updater.exe {}".format(download_url), shell=True)
        sys.exit()

from PyQt5.QtWidgets import *
from quamash import QEventLoop
from PyQt5.QtGui import QColor

import discord
import asyncio
from inspect import isawaitable

from gui import Gui
from dialogs import AuthDialog
from client import DiscordClient
from themes import themes, getThemes
from quirks import Quirks
from config import Config
from moods import Moods
from auth import UserAuth, save_auth
from formatting import *


class App(QApplication):
    def __init__(self):
        QApplication.__init__(self, sys.argv)
        # Establish loop as Quamash Event Loop
        loop = QEventLoop(self)
        self.loop = loop
        asyncio.set_event_loop(loop)

        self.themes = themes
        self.theme = themes["pesterchum2.5"]
        self.theme_name = self.theme["name"]
        self.options = Options
        self.config = Config
        self.moods = Moods
        self.setStyleSheet(self.theme["styles"])

        self.nick = None
        self.client = DiscordClient(app=self, loop=self.loop)

        self.user, self.passwd, self.token = UserAuth

        if not UserAuth[0] and not UserAuth[1] and not UserAuth[2]:
            self.openAuth()
            save_auth((self.user, self.passwd, self.token,))

        asyncio.ensure_future(self.runbot())

        self.gui = Gui(self.loop, self)

        loop.run_forever()

    def cli(self):
        """
        Runs a CLI-style eval loop, if eval(input) is awaitable (`inspect.isawaitable`)
        will await, runs in an executor
        """

        async def run_exe():
            while True:
                try:
                    line = await self.loop.run_in_executor(None, input, ">>> ")
                    evl = eval(line)
                    if isawaitable(evl):
                        r = await evl
                        print(r)
                    else:
                        print(evl)
                except Exception as e:
                    print(e)

        asyncio.ensure_future(run_exe())

    async def on_message(self, message):
        """Called on `Client.on_message`, Message handling happens here"""
        if message.content.startswith("_") and message.content.endswith("_"):
            message.content = "/me " + message.content[1:-1]
        if isinstance(message.channel, discord.PrivateChannel):
            if not message.channel.name:
                message.channel.name = ",".join(map(lambda m: m.name, message.channel.recipients))
            if message.channel.type is discord.ChannelType.group:
                tab = self.gui.start_privmsg(message.channel)
            else:
                tab = self.gui.start_privmsg(message.channel.user)
            fmt = fmt_disp_msg(self, message.content, user=message.author)
            if fmt:
                tab.display_text(fmt)
        else:
            if self.gui.memosWindow:
                if message.server in self.gui.memosWindow.open.keys():
                    fmt = fmt_disp_msg(self, message.content, user=message.author)
                    if fmt:
                        try:
                            self.gui.memosWindow.display_message(message.channel, fmt)
                        except AttributeError as e:
                            print(e)

    async def on_ready(self):
        """Called on `Client.on_ready`, generally once the client is logged in and ready"""
        self.nick = self.client.user.name
        self.quirks = Quirks(self)
        if "debug" in sys.argv:
            self.cli()
        self.gui.initialize()

    def change_mood(self, mood):
        pass

    def change_theme(self, theme):
        if theme != self.theme_name:
            self.theme = themes[theme]
            self.theme_name = self.theme["name"]
            self.setStyleSheet(self.theme["styles"])
            if hasattr(self, "gui"):
                self.gui.close()
                self.gui = Gui(self.loop, self)
                self.gui.initialize()

    def getColor(self, member, type=str):
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
        message = self.quirks.process_quirks(message)
        asyncio.ensure_future(self.client.send_message(channel, message, tts=tts))

    def openAuth(self, f=False):
        self.user, self.passwd, self.token = AuthDialog(self, self, f=f).auth
        if hasattr(self, "gui"):
            self.exit()

    async def runbot(self):
        try:
            if (self.user and self.passwd) and not self.token:
                await self.client.start(self.user, self.passwd, bot=False)
                return
            elif self.token and not (self.user or self.passwd):
                await self.client.start(self.token, bot=False)
                return
            self.exit()
        except discord.LoginFailure:
            self.openAuth(f=True)
            save_auth((self.user, self.passwd, self.token))

    def exit(self, code=0):
        """
        Called when exiting the client
        Save configurations and sys.exit
        """
        save_auth((self.user, self.passwd, self.token,))
        self.quirks.save_quirks()
        sys.exit(code)


PesterClient = App()
