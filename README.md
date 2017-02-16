# Pesterchum-Discord

A Discord client mimicking the Pesterchum chat client from Homestuck, Uses a lot of code from my Pesterchum Client

#Install
Unzip the file and run Pesterchum.exe, the GUI wont launch until connected. If there is an update, updater.exe will launch in a console.
It doesn't install anywhere, its fairly portable. It is not yet for OSX/Linux, contact me if anyone is interested in 
supporting it.

#Tokens
The Discord API has officially deprecated user logins, (email / password) best choice is to use tokens. All accounts
have tokens, to find yours:

1. Open Discord
2. Press Ctrl+Shift+i
3. Click "Application" tab
4. Expand Storage > Local Storage > https://discordapp.com
5. Find "token" under "key"
6. Copy the text in quotes on the same row

#Quirks

Pesterchum-Discord lets you do custom quirks using Regex! (Regular Expression) for help on quirks (they work identically) check out
[illuminatedWax's quirk info](https://github.com/illuminatedwax/pesterchum#quirks-1) on the original Pesterchum. Misspeller has not yet been added

Add custom quirk commands by going to the pyquirks folder and removing quirk_funcs.pyc and replacing it with your own quirk_funcs.py
(if you want parts from the original just grab the [source](https://github.com/henry232323/Pesterchum-Discord/blob/master/pyquirks/quirk_funcs.py))

#Preview

###Pesterchum2.5
![PesterchumPreview](https://raw.githubusercontent.com/henry232323/Pesterchum-Discord/master/resources/pesterchum-preview.JPG)

###Trollian
![TrollianPreview](https://raw.githubusercontent.com/henry232323/Pesterchum-Discord/master/resources/trollian-preview.JPG)

#Bugs
Please report all bugs in the [issues](https://github.com/henry232323/Pesterchum-Discord/issues). 
If the application is not starting or crashes on startup, try starting it again, if that fails, 
delete cfg/auth, cfg/config.json, cfg/options.json (and if else fails try removing quirks.json too)