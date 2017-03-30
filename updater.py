#!/usr/bin/python3
# Copyright (c) 2016-2017, rhodochrosite.xyz
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

from stat import S_IWUSR
import subprocess
import requests
import zipfile
import shutil
import sys
import os


def get_update(url):
    print("Downloading update from {}".format(url))

    if not os.path.exists("temp"):
        os.mkdir("temp")
    cachepath = "temp/master.zip"
    with open(cachepath, "wb") as f:
        print("Downloading %s" % cachepath)
        response = requests.get(url, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None:  # no content length header
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s]" % ('\u2588' * done, ' ' * (50 - done)))
                sys.stdout.flush()

    zip_ref = zipfile.ZipFile(cachepath, 'r')
    zip_ref.extractall("temp")
    zip_ref.close()

    to_copy = ["python35.zip", "resources", "themes"]
    for cfile in to_copy:
        fn = "temp/{}".format(cfile)
        if os.path.isfile(fn):
            shutil.copy(fn, "./{}".format(cfile))
        else:
            for root, dirs, files in os.walk(fn):
                rp = root[5:]
                for dir in dirs:
                    dp = "{}/{}".format(rp, dir)
                    if not os.path.exists(dp):
                        os.makedirs(dp)
                for file in files:
                    try:
                        shutil.copy("{}/{}".format(root, file), "{}/{}".format(rp, file))
                    except PermissionError as e:
                        print(e)

    def onerror(func, path, exc_info):
        if not os.access(path, os.W_OK):
            # Is the error an access error ?
            os.chmod(path, S_IWUSR)
            func(path)

    shutil.rmtree("temp", onerror=onerror)
    subprocess.Popen("start pesterchum.exe", shell=True)
    sys.exit()

if len(sys.argv) > 1:
    get_update(sys.argv[-1])
else:
    response = requests.get("https://api.github.com/repos/henry232323/pesterchum-discord/releases/latest").json()
    current_version = response["tag_name"]
    download_url = response["assets"][0]["browser_download_url"]
    get_update(download_url)