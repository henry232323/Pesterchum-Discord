import sys
from cx_Freeze import setup, Executable
import os

os.environ['TCL_LIBRARY'] = "C:\\Users\\Henry\\AppData\\Local\\Programs\\Python\\Python35-32\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Users\\Henry\\AppData\\Local\\Programs\\Python\\Python35-32\\tcl\\tk8.6"

sys.argv.append("build")

include_files = ["resources", "themes"]

build_exe_options = {
    "includes": ["PyQt5", "os", "json", "asyncio", "types", "discord", "aiohttp"],
    "excludes": ["tkinter", "_tkinter", '_gtkagg', '_tkagg', 'bsddb', 'curses',
                 'pywin.debugger', 'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl',
                 'unittest', 'idlelib'],
    "include_files": include_files,
    }

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name = "Pesterchum-Discord",
    version = "v1.0.2",
    description="A Discord client mimicking the Pesterchum chat client from Homestuck, Uses a lot of code from my Pesterchum Client.",
    options={"build_exe": build_exe_options},
    executables=[Executable("pesterchum.py", base=base, icon="resources/pc_chummy.ico"),
                 Executable("updater.py", base=None)]
        )
