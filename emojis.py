#!/usr/bin/env python
import discord
import re

class Emojis(object):
    def __init__(self, app):
        self.app = app

    @staticmethod
    def process_emojis(message):
        fmt = re.sub("<:(.*?)>", Emojis.fmt_emote, message)
        return fmt

    @staticmethod
    def fmt_emote(match):
        str = match.group(0)
        str = str[1:-1]
        name, id = str.split(":")
        emoji = discord.Emoji(id=id)
        fmt = "<img src=\"{}\"".format(emoji.url)
        return fmt
