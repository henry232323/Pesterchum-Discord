import sys
from setuptools import setup

include_files = ["resources", "themes", "README.md", "LICENSE"]

build_exe_options = {
    "includes": ["PyQt5", "os", "json", "asyncio", "types", "discord", "aiohttp", "requests"],
    "excludes": ["tkinter", "_tkinter", '_gtkagg', '_tkagg', 'bsddb', 'curses',
                 'pywin.debugger', 'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl',
                 'unittest', 'idlelib', 'certifi', 'nacl', "_lzma", "_hashlib", "_bz2"],
    "include_files": include_files,
    }

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Pesterchum-Discord",
    version="v1.0.4",
    description="A Discord client mimicking the Pesterchum chat client from Homestuck, Uses a lot of code from my Pesterchum Client.",
    author="henry232323",
    author_email="henry@henry232323",
    packages=["pyquirks"],
    url="https://github.com/henry232323/Pesterchum-Discord",
    license="GPL3",
        )
