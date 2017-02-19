#!/usr/bin/env python
import discord
import re


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
