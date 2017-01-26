import json, os

default_auth = (None, None, None)

authpath = "cfg/auth.json"

if not os.path.exists("cfg"):
    os.mkdir("cfg")
if not os.path.exists(authpath):
    with open(authpath, 'w+') as af:
        af.write(json.dumps(default_auth))
    UserAuth = default_auth
else:
    with open(authpath, 'r') as af:
        tx = af.read()
        UserAuth = json.loads(tx)


def save_auth(auth):
    with open(authpath, 'w+') as af:
        jd = json.dumps(auth)
        af.write(jd)
