#!/usr/bin/env python
import discord
import re

class Emojis(object):
    @staticmethod
    def process_emojis(message, mobj):
        fmt = re.sub("<:(.*?)>", lambda x: Emojis.fmt_emote(x, mobj), message)
        return fmt

    @staticmethod
    def fmt_emote(match, mobj):
        str = match.group(0)
        str = str[2:-1]
        name, id = str.split(":")
        emoji = discord.Emoji(id=id, server=mobj.server)
        fmt = '<img src="{}"/>'.format(emoji.url)
        return fmt
