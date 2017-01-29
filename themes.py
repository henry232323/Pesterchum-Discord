import os

themes = dict()

def getThemes(themes):
    '''
    Can be called any time to refresh themes, creates a theme
    for every folder in the themes directory, sets the css file to
    foldername.css
    The folder name defines the Theme name
    All uis located in the ui folder
    More support for themes to come
    '''
    themedir = os.listdir("themes")
    for theme in themedir:
        if os.path.isdir("themes/"+theme):
            themes[theme] = dict()
            name = theme + ".css"
            fpath = os.path.join("themes", theme, name)
            path = os.path.join("themes", theme)
            uipath = os.path.join("themes", theme, "ui")
            with open(fpath, "r") as tfile:
                rfile = tfile.read()
            themes[theme]["styles"] = rfile.replace("$path", path.replace("\\", "/"))
            themes[theme]["style_file"] = name
            themes[theme]["style_path"] = fpath
            themes[theme]["path"] = path
            themes[theme]["name"] = theme
            themes[theme]["ui_path"] = uipath
            themes[theme]["ui_dir"] = os.listdir(uipath)

getThemes(themes)
