#!/usr/bin/env python3
# Copyright (c) 2016-2020, henry232323
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

from importlib import reload
from random import choice
import inspect
import json
import re
import os

import pyquirks


class Quirks(object):
    def __init__(self, app):
        self.app = app
        self.id = self.app.client.user.id
        if not os.path.exists("cfg/quirks.json"):
            with open("cfg/quirks.json", 'w') as qf:
                qf.write(json.dumps({self.id:list()}, indent=4))
        with open("cfg/quirks.json", 'r') as qf:
            self.allquirks = json.loads(qf.read())

        if str(self.id) not in self.allquirks.keys():
            self.allquirks[str(self.id)] = list()
        self.quirks = self.allquirks[str(self.id)]
        self.qfuncs = dict(inspect.getmembers(pyquirks.quirk_funcs, inspect.isfunction))

    def process_quirks(self, message):
        try:
            fmt = message
            for type, quirk in self.quirks:
                if type == "prefix":
                    fmt = quirk + fmt
                elif type == "suffix":
                    fmt += quirk
                elif type == "replace":
                    fmt = fmt.replace(quirk[0], quirk[1])
                elif type == "regex":
                    fmt = re.sub(quirk[0], quirk[1], fmt)
                    for name, func in self.qfuncs.items():
                        if name in quirk[1]:
                            def callfunc(match):
                                return func(match.group(0)[len(name)+1:-1])
                            fmt = re.sub(r"({}\(.*?\))".format(name), callfunc, fmt)
                elif type == "random":
                    def random(match):
                        return re.sub(quirk[0], choice(quirk[1]), match.group(0))
                    fmt = re.sub(quirk[0], random, fmt)
                    for name, func in self.qfuncs.items():
                        if name in quirk[1]:
                            def callfunc(match):
                                return func(match.group(0)[len(name)+1:-1])
                            fmt = re.sub(r"({}\(.*?\))".format(name), callfunc, fmt)
            return fmt
        except Exception as e:
            print(e)

    def save_quirks(self):
        with open("cfg/quirks.json", 'w') as qf:
            qf.write(json.dumps(self.allquirks, indent=4))

    def append(self, item):
        self.quirks.append(item)

    def reload(self):
        reload(pyquirks)
        self.qfuncs = dict(inspect.getmembers(pyquirks.quirk_funcs, inspect.isfunction))