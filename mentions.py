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

class Mentions(object):
    @staticmethod
    def process_mentions(message, mobj):
        for mention, member in zip(mobj.raw_mentions, mobj.mentions):
            message = message.replace("<@{}>".format(mention), Mentions.fmt_mention(mention, member))
        for mention, channel in zip(mobj.raw_channel_mentions, mobj.channel_mentions):
            message = message.replace("<#{}>".format(mention), Mentions.fmt_channel(mention, channel))
        for mention, role in zip(mobj.raw_role_mentions, mobj.role_mentions):
            message = message.replace("<@&{}>".format(mention), Mentions.fmt_role(mention, role))
        return message

    @staticmethod
    def fmt_mention(mention, member):
        fmt = '<a href="mention={member.id}">@{member.display_name}</a>'.format(member=member)
        return fmt

    @staticmethod
    def fmt_channel(mention, channel):
        fmt = '<a href="channel={channel.id}">#{channel.name}</a>'.format(channel=channel)
        return fmt

    @staticmethod
    def fmt_role(mention, role):
        fmt = '<a href="role={role.id}" style="color: {role.color}">@{role.name}</a>'.format(role=role)
        return fmt
