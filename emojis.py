#!/usr/bin/env python3
# Copyright (c) 2016-2017, henry232323
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


import re
import unicodedata


class Emojis(object):
    def __init__(self, bot):
        self.bot = bot

    def process_emojis(self, message, mobj):
        fmt = re.sub(r"/<:.*?:(\d+)>/", lambda x: self.fmt_emote(x, mobj), message)
        fmt = re.sub(r":[\w]*?:", lambda x: self.fmt_emoji(x, mobj), fmt)
        return fmt

    def fmt_emote(self, match, mobj):
        str = match.group(0)
        str = str[2:-1]
        _name, id = str.split(":")
        emoji = self.bot.get_emoji(id)
        fmt = '<img src="{}"/>'.format(emoji.url)
        return fmt

    def fmt_emoji(self, match, mobj):
        str = match.group(0)
        name = str[1:-1]
        try:
            return unicodedata.lookup(name.upper())
        except KeyError:
            print(name)
            return str
