import sys, os, shutil
import zipfile
import urllib.request
import subprocess
import requests


def update(version):
    response = requests.get("https://api.github.com/repos/henry232323/pesterchum-discord/releases/latest").json()
    current_version = response["tag_name"]
    if current_version > version:
        download_url = response["assets"][0]["browser_download_url"]
        get_update(download_url)


def get_update(url):
    urlresp = urllib.request.urlopen(url)
    data = urlresp.read()

    if not os.path.exists("temp"):
        os.mkdir("temp")
    cachepath = "temp/master.zip".format()
    with open(cachepath, "wb") as df:
        df.write(data)

    zip_ref = zipfile.ZipFile(cachepath, 'r')
    zip_ref.extractall("temp")
    zip_ref.close()

    def del_rw(*args):pass

    cp = "temp"
    for root, dirs, files in os.walk(cp):
        rp = root[len(cp) + 1:]
        for dir in dirs:
            dp = "{}/{}".format(rp, dir)
            if not os.path.exists(dp):
                os.makedirs(dp)

        for file in files:
            if file == "updater.py":
                continue
            try:
                shutil.copy(root + "/" + file, "{}/{}".format(rp, file))
            except PermissionError as e:
                pass

    shutil.rmtree("temp", onerror=del_rw)
    subprocess.call("start pesterchum.exe")
    sys.exit()
