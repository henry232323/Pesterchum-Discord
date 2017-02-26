#!/usr/bin/env python
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
