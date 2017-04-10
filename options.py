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

import json
import os

default_options = {
    "chum_list":{
        "hide_offline_chums":False,
        "show_empty_groups":False,
        "show_number_of_online_chums":False,
        "sort_chums":0,
        "low_bandwidth":False
        },
    "conversations":{
        "time_stamps":True,
        "clock_type":1,
        "show_seconds":False,
        "op_and_voice_in_memos":False,
        "use_animated_smilies":False,
        "receive_random_encounters":False,
        },
    "interface":{
        "tabbed_conversations":True,
        "tabbed_memos":True,
        "minimize":0,
        "close":1,
        "blink_taskbar_on_pesters":False,
        "blink_taskbar_on_memos":False,
        "auto_update":False,
        },
    "theme":{
        "theme":"pesterchum2.5"
        }
    }

if not os.path.exists("cfg"):
    os.mkdir("cfg")
if not os.path.exists("cfg/options.json"):
    with open("cfg/options.json", 'w+') as options:
        options.write(json.dumps(default_options, indent=4))
confpath = "cfg/options.json"
if os.path.exists(confpath):
    with open(confpath, 'r') as options:
        data = options.read()
    Options = json.loads(data)
    opt_keys = Options.keys()
    for key in default_options.keys():
        if key not in opt_keys:
            Options[key] = default_options[key]
        else:
            opt_keys_2 = Options[key].keys()
            for key in default_options[key].keys():
                if key not in opt_keys_2:
                    Options[key][key] = default_options[key][key]
else:
    with open(confpath, 'w') as options:
        options.write(json.dumps(default_options, indent=4))

    with open(confpath, 'r') as options:
        data = options.read()
    Options = json.loads(data)


def save_options(options):
    with open("cfg/options.json", 'w') as conffile:    
        conffile.write(json.dumps(options, indent=4))
