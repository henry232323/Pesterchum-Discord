import sys, os, shutil
import zipfile
import urllib
import subprocess

downloadurl = "https://github.com/henry232323/Pesterchum-Discord/archive/master.zip"
urlresp = urllib.request.urlopen(downloadurl)
data = urlresp.read()

if not os.path.exists("temp"):
    os.mkdir("temp")
cachepath = "temp/master.zip".format()
with open(cachepath, "wb") as df:
    df.write(data)

zip_ref = zipfile.ZipFile(cachepath, 'r')
zip_ref.extractall("temp")
zip_ref.close()


def del_rw(action, name, exc):
    os.chmod(name, stat.S_IWRITE)
    os.remove(name)

cp = "temp/Pesterchum-Discord-master"
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

subprocess.call("python pesterchum.py")
sys.exit()
