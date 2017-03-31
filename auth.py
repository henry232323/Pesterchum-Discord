#!/usr/bin/python3
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

import base64
import json
import os

default_auth = (None, None, None, False)

authpath = "cfg/auth"

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
            UserAuth = (None, None, None, False)

if len(UserAuth) < len(default_auth):
    UserAuth = default_auth

def save_auth(auth):
    with open(authpath, 'wb+') as af:
        jd = base64.b64encode(json.dumps(auth).encode())
        af.write(jd)
