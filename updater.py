import sys, os, shutil
import zipfile
import requests
import subprocess
from stat import S_IWUSR


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

    shutil.copy("temp/python35.zip", "./python35.zip")
    def onerror(func, path, exc_info):
        if not os.access(path, os.W_OK):
            # Is the error an access error ?
            os.chmod(path, S_IWUSR)
            func(path)

    shutil.rmtree("temp", onerror=onerror)
    subprocess.Popen("start pesterchum.exe", shell=True)
    sys.exit()

try:
    get_update(sys.argv[-1])
except IndexError:
    response = requests.get("https://api.github.com/repos/henry232323/pesterchum-discord/releases/latest").json()
    current_version = response["tag_name"]
    download_url = response["assets"][0]["browser_download_url"]