import json, os
import base64

default_auth = (None, None, None)

authpath = "cfg/auth.json"

if not os.path.exists("cfg"):
    os.mkdir("cfg")
if not os.path.exists(authpath):
    with open(authpath, 'wb+') as af:
        af.write(base64.b64encode(json.dumps(default_auth).encode()))
    UserAuth = default_auth
else:
    with open(authpath, 'r') as af:
        tx = af.read()
        try:
            UserAuth = json.loads(base64.b64decode(tx).decode())
        except (UnicodeDecodeError, json.decoder.JSONDecodeError):
            UserAuth = (None, None, None)

def save_auth(auth):
    with open(authpath, 'wb+') as af:
        jd = base64.b64encode(json.dumps(auth).encode())
        af.write(jd)
