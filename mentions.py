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


class Mentions(object):
    @staticmethod
    def process_mentions(text, message):
        fin = text
        for member in message.mentions:
            fin = text.replace(member.mention, f'<a href="mention={member.id}">@{member.display_name}</a>')
        for channel in message.channel_mentions:
            fin = text.replace(channel.mention, f'<a href="channel={channel.id}">#{channel.name}</a>')
        for role in message.role_mentions:
            fin = text.replace(role.mention, f'<a href="role={role.id}" style="color: {role.color}">@{role.name}</a>')
        return fin

    @staticmethod
    def fmt_mention(member):
        return f'<a href="mention={member.id}">@{member.display_name}</a>'

    @staticmethod
    def fmt_channel(channel):
        return f'<a href="channel={channel.id}">#{channel.name}</a>'

    @staticmethod
    def fmt_role(role):
        return f'<a href="role={role.id}" style="color: {role.color}">@{role.name}</a>'
