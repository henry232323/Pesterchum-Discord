import json
import re
import os
import inspect
from random import choice

from pyquirks import quirk_funcs


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

    def process_quirks(self, message):
        try:
            fmt = message
            funcs = dict(inspect.getmembers(quirk_funcs, inspect.isfunction))
            for type, quirk in self.quirks:
                if type == "prefix":
                    fmt = quirk + fmt
                elif type == "suffix":
                    fmt += quirk
                elif type == "replace":
                    fmt = fmt.replace(quirk[0], quirk[1])
                elif type == "regex":
                    # quirk[0] = eval(quirk[1], funcs)
                    # re.sub(r"\\([0-9]+)",r"\\g<\1>",uinput)
                    fmt = re.sub(quirk[0], quirk[1], message)
                    print(quirk, message)
                    print(fmt)
                elif type == "random":
                    fmt = re.sub(quirk[0], choice(quirk[1]), message)
            return fmt
        except Exception as e:
            print(e)

    def save_quirks(self):
        with open("cfg/quirks.json", 'w') as qf:
            qf.write(json.dumps(self.allquirks))