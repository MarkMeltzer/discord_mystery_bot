# Description
This is a small python based discord bot for use in a discord murder mystery game. It spins up a discord bot and a flask server. The flask local server can be used as an http api endpoint to send commands to the discord bot. Any other application (for example a gamemaker based game) can send http GET request to this local server to force the discord bot to do certain actions.

Currently the bot supports setting a party of players and moving these players around voice channels.

# Requirements
- python 3.6 or higher
    - Can be downloaded at: https://www.python.org/downloads/
- discord bot token
    - Can be requested at: https://discord.com/developers/applications
- discord.py python module
    - Can be installed using pip with the following command: ***python -m pip install discord.py***
- flask python module
    - Can be installed using pip with the following command: ***python -m pip install flask***

# How to use
##### How to run the bot:
1. Download the script and the contents of this repository (using the green ***Code*** button and ***Download zip***). Extract the contents of the zip anywhere.
2. Edit the *config.txt* (instructions in the file).
2. Launch a commandprompt in the directory containing the extracted files and run the script with the following command: ***python discord_mystery_bot.py***
3. The bot should report that it is up and running in discord. You are now ready to use it.

##### How to use the bot:
- Whenever the bot should set the current party, send the following http GET request: ***http://localhost:5335/setparty***
- Whenever the bot should move the current to a different voice channel, send the following http GET request: ***http://localhost:5335/movetoroom?room=[ROOM]*** where ***[ROOM]*** is the name of the voice channel to move to (case-sensitive).
- Sending ***exit*** in the discord server the bot is operating in will shutdown the bot.
- Sending ***listchannels*** in the discord server the bot is operating in will list the channels in the current server in discord.
- Sending ***listguilds*** in the discord server the bot is operating in will list the servers the bot is currently operating in.
- Sending ***currentparty*** in the discord server the bot is operating in will list the current party members in the current server in discord.

# Todo
- Freeze code into a executable to make using the bot more user friendly.
- Make IP/port configurable.
- Add proper error handeling.
- Exit the flask server when exiting the bot.