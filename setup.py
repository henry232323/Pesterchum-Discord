import sys
from cx_Freeze import setup, Executable
import os

os.environ['TCL_LIBRARY'] = "C:\\Users\\Henry\\AppData\\Local\\Programs\\Python\\Python35-32\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Users\\Henry\\AppData\\Local\\Programs\\Python\\Python35-32\\tcl\\tk8.6"

sys.argv.append("build")

include_files = ["resources", "themes", "cfg"]

build_exe_options = {
    "includes":["PyQt5", "os", "json", "asyncio", "types"],
    "excludes":["tkinter", "_tkinter", '_gtkagg', '_tkagg', 'bsddb', 'curses',
            'email', 'pywin.debugger',
            'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl'],
    "packages":["oyoyo"],
    "include_files":include_files,
    }

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name = "Pesterchum-3.5",
    version = "3.5-0.1.0",
    description = "A version of ghostDunk/illuminatedWax's Pesterchum client, built using Asyncio, PyQt5, and Python 3.5. A server specific IRC client built to imitate the Pesterchum chat client as seen in Homestuck.",
    options = {"build_exe": build_exe_options},
    executables = [Executable("pesterchum.py", base=base, icon="resources/pc_chummy.ico", requires=['PyQt5'])]
        )
        
                        
