from PyQt5.QtWidgets import *
from quamash import QEventLoop

import asyncio
import sys
from inspect import isawaitable

import discord

from gui import Gui
from dialogs import AuthDialog
from client import DiscordClient
from themes import themes, getThemes
from options import Options
from config import Config
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
        self.setStyleSheet(self.theme["styles"])

        self.nick = None
        self.client = DiscordClient(app=self, loop=self.loop)

        self.user, self.passwd, self.token = UserAuth

        if not UserAuth[0] and not UserAuth[1] and not UserAuth[2]:
            self.openAuth()
            save_auth((self.user, self.passwd, self.token,))

        self.runbot()

        self.gui = Gui(self.loop, self)

        if "debug" in sys.argv:
            self.cli()

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
        self.gui.initialize()

    def change_theme(self, theme):
        if theme != self.theme_name:
            self.theme = themes[theme]
            self.theme_name = self.theme["name"]
            self.setStyleSheet(self.theme["styles"])
            if hasattr(self, "gui"):
                self.gui.close()
                self.gui = Gui(self.loop, self)
                self.gui.initialize()

    def getColor(self, member):
        """Get the given primary role color for a `Member`, returns a `Discord.Color` instance"""
        if hasattr(member, "roles"):
            clr = member.roles[0].color
            return "rgb({clr.r},{clr.g},{clr.b}".format(clr=clr)

    def send_msg(self, message, channel):
        """Send message `message` to the User, Private Channel, or Channel `channel`"""
        asyncio.ensure_future(self.client.send_message(channel, message))

    def openAuth(self):
        self.user, self.passwd, self.token = AuthDialog(self, self).auth

    def runbot(self):
        if self.user and self.passwd and not self.token:
            asyncio.ensure_future(self.client.start(self.user, self.passwd))
        elif self.token and not (self.user or self.token):
            asyncio.ensure_future(self.client.start(self.token))
        else:
            print("You broke it?")
            self.exit(code=1)

        if hasattr(self, "gui"):
            self.exit()

    def exit(self, code=0):
        """
        Called when exiting the client
        Save configurations and sys.exit
        """
        save_auth((self.user, self.passwd, self.token,))
        sys.exit(code)


PesterClient = App()
