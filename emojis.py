#!/usr/bin/python3
# Copyright (c) 2016-2017, rhodochrosite.xyz
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

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
