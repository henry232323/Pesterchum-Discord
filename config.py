#!/usr/bin/env python
from random import randint
import json, os

#If a username is not defined, generate a random 'pesterClient' name
uname = "pesterClient" + str(randint(100, 700))
#Generic template config, used if config is missing or empty
template_config = dict(users={uname:"#000000"},
                   defaultuser=uname,
                   friends=dict(),
                   lastTheme="pesterchum2.5",
                   timestamp_show_seconds=False,
                   userlist=dict(),
                   blocked=list()) 

if not os.path.exists("cfg"):
    os.mkdir("cfg")
if not os.path.exists("cfg/config.json"):
    with open("cfg/config.json", 'w+'):
        pass
with open("cfg/config.json", 'r') as config:
    data = config.read()
if data:
    #If missing any data, fill in from the template
    Config = json.loads(data)
    conf_keys = Config.keys()
    for key in template_config.keys():
        if key not in conf_keys:
            Config[key] = template_config[key]
else: #In case we need to reference the template again
    Config = {key:value for key,value in template_config.items()}

def save_config(config):
    with open("cfg/config.json", 'w') as conffile:    
        conffile.write(json.dumps(config))  
