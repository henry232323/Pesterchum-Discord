import sys, os, shutil
import zipfile
import requests
import subprocess

def get_update(url):
    sys.stdout.write("Downloading update from {}".format(url))

    if not os.path.exists("temp"):
        os.mkdir("temp")
    cachepath = "temp/master.zip".format()
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
    subprocess.call("start pesterchum.exe", shell=True)
    sys.exit()

get_update(sys.argv[-1])
