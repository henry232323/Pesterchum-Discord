# Looking for Contributors!
I no longer have the time to maintain this project, if you are interested in contributing let me know!

# Pesterchum-Discord
A Discord client mimicking the Pesterchum chat client from Homestuck, for the few people who are still interested in that.

If you have any questions either contact me the github or add me at Henry#8808 on Discord.

This app is NOT an all-in-one client! It is meant to enhance RP and anything else you wish to do with it, however
it is recommended you still use regular Discord for technical functions.

### Donate
If you like what I've made, consider [buying me a coffee](https://ko-fi.com/A372XXA)

# Install
The release download is distributed as a .zip file. Unzip the file and inside will be a file called `pesterchum.exe`
If there is an update, updater.exe will launch in a console.
It doesn't install anywhere, its fairly portable. It is not yet for OSX/Linux, contact me if anyone is interested in 
supporting it.

If you are running an older version and would like to update (> v1.0.6) you can enable the auto updater
by going into your `cfg/options.json` and changing the value `"auto_update": false` to `"auto_update": true`

# Updating
Auto updating by default is disabled, but can be enabled in settings, if you would rather manually install the new
update, copy and replace the following files and folders into the old installation
`discord, pesterchum.exe, updater.exe, python3.6.zip, python3.6.dll, asyncio, pywintypes36.dll`
If there are new themes or quirks, copy the relevant files / folders into the `pyquirks` folder and the `themes` folder

# Tokens
The Discord API no longer allows use of login credentials! Once you update to v1.3.0 or later you MUST use a token. All accounts
have tokens, [here](https://discordhelp.net/discord-token)'s how to find yours.



# Quirks
Pesterchum-Discord lets you do custom quirks using Regex! (Regular Expression) for help on quirks (they work identically) check out
[illuminatedWax's quirk info](https://github.com/illuminatedwax/pesterchum#quirks-1) on the original Pesterchum. Misspeller has not yet been added. Works similarly to how its documented [here](https://github.com/illuminatedwax/pesterchum/blob/master/PYQUIRKS.mkdn), you do NOT need to add the `function.command = "name"`

Add custom quirk commands by going to the pyquirks folder and removing quirk_funcs.pyc and replacing it with your own quirk_funcs.py
(if you want parts from the original just grab the [source](https://github.com/henry232323/Pesterchum-Discord/blob/master/pyquirks/quirk_funcs.py))

# Bugs
Please report all bugs in the [issues](https://github.com/henry232323/Pesterchum-Discord/issues). 
If the application is not starting or crashes on startup, try starting it again, if that fails, 
delete cfg/auth, cfg/config.json, cfg/options.json (and if else fails try removing quirks.json too)

# Themes
While I've made every theme available so far, they're easy (ish) for anyone to make. If you'd like
me to add a theme, just send a pull request or message me.
If you want to make a theme, best chance is to reverse engineer the already available (in the source) 
.ui files of an existing theme.
 <br /><br />
All themes have several main parts:
##### theme.json
 ```json
{
  "name": "Pesterchum",
  "ui_path": "ui",
  "inherits": "Pesterchum 2.5",
  "css": "pesterchum.css"
}
 ```
 This file is found in the theme folder. Name the folder whatever you'd like, that doesn't matter, 
 for example this is in the `themes/Pesterchum` folder. 
 In your folder there are several things. 
 - A folder (designated in the `theme.json`) with your UI's in it, 
 this one has its in `themes/Pesterchum/ui` as designated in the file `"ui_path": "ui"` 
 - All your image files, look at the other themes for examples. These must be `.png`'s, eventually 
 I'll map out where every image is needed, for now its pretty easy to figure out.
 - Your css / styles, this is the file that is used to decorate your theme, just like a webpage, and
 is designated in your `theme.json`, in this one it is set to the path `themes/Pesterchum/pesterchum.css`
 with the line `"css": "pesterchum.css"` Look at example css to figure out how to use IDs and Classes 
 in your css to match with the UIs, for example the main window can be targeted with `.Gui` or `.QMainWindow`
 
 The `theme.json` will designate four things, like mentioned above
 - `name` The name of the theme (as displayed in the options)
 - `ui_path` The relative path in the folder to find the ui's
 - `inherits` Which theme's css it will inherit (for example Pesterchum inherits Pesterchum 2.5)
 - `css` The relative path to the css file with the themes styles
 
 Make sure all relative paths do not start with a `/` 
 
 Another note, in order to designate the associated mood with the button, the mood button must be 
 checkable and called moodButton# where # is a number between 0 and 22 designating to the position in this list minus 1
 ```python
 ["chummy", "rancorous", "offline", "pleasant", "distraught",
 "pranky", "smooth", "ecstatic", "relaxed", "discontent",
 "devious", "sleek", "detestful", "mirthful", "manipulative",
 "vigorous", "perky", "acceptant", "protective", "mystified",
 "amazed", "insolent", "bemused"]
 ```
 For example moodButton0 would be the button for "Chummy" or moodButton2 would reference Offline / Abscond.
 The text on the button will remain and does not matter.
### Pesterchum 2.5
![PesterchumPreview2](https://raw.githubusercontent.com/henry232323/Pesterchum-Discord/master/resources/pesterchum2.5-preview.png)

### Trollian 2.5
![TrollianPreview](https://raw.githubusercontent.com/henry232323/Pesterchum-Discord/master/resources/trollian2.5-preview.png)

### Pesterchum
![PesterchumPreview](https://raw.githubusercontent.com/henry232323/Pesterchum-Discord/master/resources/pesterchum-preview.png)

### Serious Business
![DadPreview](https://raw.githubusercontent.com/henry232323/Pesterchum-Discord/master/resources/dad-preview.png)

### sbahj
![sbahjPreview](https://raw.githubusercontent.com/henry232323/Pesterchum-Discord/master/resources/sbahj-preview.png)

