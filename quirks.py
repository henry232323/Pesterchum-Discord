#!/usr/bin/env python
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
                qf.write(json.dumps({self.id:list()}))
        with open("cfg/quirks.json", 'r') as qf:
            self.allquirks = json.loads(qf.read())

        if self.id not in self.allquirks.keys():
            self.allquirks[self.id] = list()
        self.quirks = self.allquirks[self.id]
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
            qf.write(json.dumps(self.allquirks))

    def append(self, item):
        self.quirks.append(item)

    def reload(self):
        reload(pyquirks)
        self.qfuncs = dict(inspect.getmembers(pyquirks.quirk_funcs, inspect.isfunction))