# Hv-PugBot
Hv-PugBot is a multichannel discord bot for pickup games organisation. This is a modified version of PuboBot which is also credited here in this readme, along with a link to their support discord.
Bot keeps a statistic database, has features to automatically remove AFK users, disallow users to play pickups, fun phrases, team picking and more!

# Requirements
Python==3.6+
aiohttp==3.6.2
anyreadline==0.1.1
async-timeout==3.0.1
attrs==19.3.0
chardet==3.0.4
discord.py==1.3.1
idna==2.8
multidict==4.7.4
pyreadline==2.1
sqlite3-api==1.0.4
websockets==8.1
yarl==1.4.2

**# Tutorial for a FRESH install:

1. Upgrade system pip:
python -m pip install --upgrade pip

2  Upgrade user pip:
python -m pip install --user --upgrade pip

3 . Verify Global is up to date:
python -m pip --version



`**` YOU CAN SKIPP THIS TO THE NEXT `**`'s

4. Create a 'virtual environment' in folder 'env'.  You can do full
paths to elsewhere if needed:

python -m venv env

You'll see bunch of folder/files made there now in the 'env' folder

5. Activate/use this environment in your shell:
env\Scripts\activate

6. Verify it's in use:
where python

D:\tmp\env\Scripts\python.exe

See the python we use is now in our env folder.

7. Uprade the pip of our env (yes it was created with old now we update)
python -m pip install --upgrade pip
`***** END OF SKIP ********`
_________________________________________________

8. Installs, Always put this in:
pip install wheel

9. Installs, For discord:
pip install readline <--linux
pip install pyreadline <--windows
pip install requests
pip install discord.py


`** YOU CAN SKIPP THIS TO THE NEXT **'s`

Note: the sqlite3 that discord mentions as a dep is inbuilt to python 3.
10. Make our notes to ourselves, we need these it's a must:
python --version > python-version-used.txt
python -m pip freeze > requirements.txt

Reproduce our production environment later, on diff box, etc:
11. Make an env as above tutorial steps 1 thru and including 6.  You *MUST*
use the *SAME* version of python that your master used.  That's why we made
the 'python-version-used.txt'

11. Now the env is setup.  Now let's make it fully reproducable:
Copy over the requirements.txt file to same folder that houses the 'env'

12. Let's use our env pip to restore these packages:
python -m pip install -r requirements.txt

13. Copy over pubobot to same dir that houses the 'env'
`************ END OF SKIP ************`
_____________________________________________________________

14. Run pubobot.py Profit!

15. IF PUBOBOT DOESNT RUN DUE TO A CERT ISSUE !!  -- Run as admin cmd -- certutil -generateSSTFromWU roots.sst && certutil -addstore -f root roots.sst && del roots.sst


# Running
1. Fill your discord bot token or username and password in the 'config.cfg' file.
2. Run './pubobot.py' to launch the program.
3. Invite your bot to the desired server.
4. Type '!enable_pickups' on the desired channel.

# Getting help
You can find help or test the bot on the Pubobot developement server: https://discord.gg/rjNt9nC

# Credits
Developer: Leshka. You can contact me via e-mail leshkajm@ya.ru, on discord (Leshaka#8570) or pm 'Leshaka' on irc.quakenet.org server.   
Help: #warsow.pickup admin team.   
Special thanks to Mute and Perrina.
Hv for blood discord modifications, additional commands for UT2004 pugs
Nolja for his help also ;)

# License
Copyright (C) 2015 Leshka.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License version 3 as published by
the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

See 'GNU GPLv3.txt' for GNU General Public License.
