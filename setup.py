#!/usr/bin/env python3
# Copyright (c) 2016-2020, henry232323
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

from cx_Freeze import setup, Executable
import sys, os

sys.argv.append("build")

include_files = ["resources", "themes", "README.md", "LICENSE"]

includes = ["PyQt5", "os", "json", "types", "discord", "aiohttp",
            "requests", "contextlib", "io", "inspect", "traceback", "subprocess",
            "async_timeout", "asyncio", "asyncio.base_futures",
            "asyncio.base_events", "asyncio.base_tasks", "asyncio.base_subprocess",
            "asyncio.proactor_events", "asyncio.constants", "asyncio.selector_events",
            "asyncio.windows_utils", "idna.idnadata", "quamash", "asyncio.format_helpers",
            "asyncio.sslproto", "idna_ssl", "ssl", "_ssl"]

pcicon = None
updicon = None

if os.name == "posix":
    includes.append("idna.idnadata")
    pcicon = "resources/pc_chummy.icns"
    updicon = "resources/sburb.icns"

build_exe_options = {
    "includes": includes,
    "excludes": ["tkinter", "_tkinter", '_gtkagg', '_tkagg', 'bsddb', 'curses',
                 'pywin.debugger', 'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl',
                 'unittest', 'idlelib', 'nacl', "_lzma", "_hashlib", "_bz2"],
    "include_files": include_files,
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"
    pcicon = "resources/pc_chummy.ico"
    updicon = "resources/sburb.ico"

if sys.platform == "win32":
    PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
    build_exe_options['include_files'] += [
        os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'libcrypto-1_1-x64.dll'),
        os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'libssl-1_1-x64.dll'),
    ]

setup(
    name="Pesterchum-Discord",
    version="1.3.7",
    description="Pesterchum Client",
    options={"build_exe": build_exe_options},
    executables=[
        Executable("pesterchum.py", base=base, icon=pcicon),
        Executable("updater.py", base=None, icon=updicon)
    ]
)
