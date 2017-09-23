#!/usr/bin/env python3
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

import os
import json

themes = dict()


def getThemes(themes):
    """
    Can be called any time to refresh themes, creates a theme
    for every folder in the themes directory, sets the css file to
    `foldername`.css
    The folder name defines the Theme name
    All uis located in the ui folder
    More support for themes to come
    """
    themedir = os.listdir("themes")
    for theme in themedir:
        try:
            path = os.path.join("themes", theme)
            if os.path.isdir(path):
                conf_path = os.path.join(path, "theme.json")
                if not os.path.exists(conf_path):
                    continue
                with open(conf_path, "r") as tf:
                    theme_conf = json.loads(tf.read())
                theme_dict = dict()
                css_path = os.path.join(path, theme_conf["css"])
                ui_path = os.path.join(path, theme_conf["ui_path"])
                with open(css_path, "r") as tfile:
                    rfile = tfile.read()
                styles = rfile.replace("$path", path.replace("\\", "/"))
                theme_dict["styles"] = styles
                theme_dict["style_file"] = css_path
                theme_dict["style_path"] = css_path
                theme_dict["path"] = path
                theme_dict["name"] = theme_conf["name"]
                theme_dict["ui_path"] = ui_path
                theme_dict["ui_dir"] = os.listdir(ui_path)
                theme_dict["inherits"] = theme_conf["inherits"]
                themes[theme_conf["name"]] = theme_dict
        except Exception as e:
            print(e)
            continue

        for data in themes.values():
            if data["inherits"]:
                try:
                    data["styles"] = "\n".join([themes[data["inherits"]]["styles"], data["styles"]])
                except Exception:
                    continue
    return themes
themes = getThemes(themes)
