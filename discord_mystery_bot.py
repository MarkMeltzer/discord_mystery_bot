import discord
import threading
import time
import flask
import asyncio

############ Discord bot stuff ############

# parse the configuration file
with open("config_dev.txt") as configfile:
    config = {line.split("=")[0].strip() : line.split("=")[1].strip() for line in configfile if len(line.strip()) and not line[0] == "#"}

# global settings variables
TOKEN = config["TOKEN"]
SERVER_NAME = config["SERVER_NAME"]
MAIN_TEXTCHANNEL_NAME = config["MAIN_TEXTCHANNEL_NAME"]
PARTY_VOICECHANNEL_NAME = config["PARTY_VOICECHANNEL_NAME"]

# global variables which are set later
SERVER = None
MAIN_TEXTCHANNEL = None
DISCORD_ASYNCIO_LOOP = None
PARTY_MEMBERS = []

# create discord bot client
client = discord.Client()

@client.event
async def on_ready():
    """
        Initializes discord bot.
    """

    # set the global for the server the bot should operate on
    global SERVER
    SERVER = discord.utils.get(client.guilds, name=SERVER_NAME)

    # set the global for the main text channel through which the bot will communicate
    global MAIN_TEXTCHANNEL
    MAIN_TEXTCHANNEL = discord.utils.get(SERVER.channels, name=MAIN_TEXTCHANNEL_NAME)

    # set the global for the asyncio loop
    global DISCORD_ASYNCIO_LOOP
    DISCORD_ASYNCIO_LOOP = asyncio.get_event_loop()

    print("Up and ready in the console")
    await MAIN_TEXTCHANNEL.send(f"Up and ready in discord!!@")

@client.event
async def on_message(message):
    """
        Parses messages sent by any user.
    """

    # shutdown the bot from discord
    if message.content == "exit":
        print("Exiting bot...")
        await MAIN_TEXTCHANNEL.send("Exiting bot...")
        await client.logout()
    
    # list all channels in current guild
    if message.content == "listchannels":
        await MAIN_TEXTCHANNEL.send(f"Channels in {SERVER}: \n" + str(SERVER.channels).replace(',',',\n'))

    # list all guilds of the current client
    if message.content == "listguilds":
        await MAIN_TEXTCHANNEL.send(f"Guilds in {client}: \n" + str(client.guilds).replace(',',',\n'))

    # list the current party
    if message.content == "currentparty":
        await MAIN_TEXTCHANNEL.send("Current party: " + ", ".join([member.name for member in PARTY_MEMBERS]))

@client.event
async def set_party():
    """
        Sets the members of the current playing party to everyone in PARTY_VOICECHANNEL when
        this function is called.
    
    """

    global PARTY_MEMBERS
    
    # get the voice channel containing current party members
    party_voicechannel = discord.utils.get(SERVER.channels, name=PARTY_VOICECHANNEL_NAME)
    if not party_voicechannel:
        await MAIN_TEXTCHANNEL.send(f"{PARTY_VOICECHANNEL_NAME} voice channel not found.")
        return

    # set the party members
    PARTY_MEMBERS = party_voicechannel.members
    await MAIN_TEXTCHANNEL.send("New party: " + ", ".join([member.name for member in PARTY_MEMBERS]))

@client.event
async def move_to_room(room):
    """
        Moves the current party to a given room.
    """

    # find the destination voice channel
    destination_channel = discord.utils.get(SERVER.channels, name=room)
    if not destination_channel:
        await MAIN_TEXTCHANNEL.send(f"Destination voice channel not found!")
        return

    # move the members of the voice channel
    for member in PARTY_MEMBERS:
        await member.move_to(destination_channel)

    await MAIN_TEXTCHANNEL.send(f"Moved to room: {room}")

def discord_run():
    """
        Runs the client. Used as wrapper for threading.
    """

    client.run(TOKEN)
    
# run discord bot in new thread
discord_thread = threading.Thread(target=discord_run)
discord_thread.start()

############ Flask Stuff ############
app = flask.Flask(__name__)

@app.route('/')
def index():
    """
        Main page, mainly used for testing.
    """

    return "Yeah its working my man"

@app.route('/movetoroom')
def api_movetoroom():
    """
        API endpoint for moving the current party to a certain room.
        Should be used as:
            adress:port/movetoroom?[ROOM]
        where [ROOM] is the name of the voicechannel the party should be moved to.
    """

    args = flask.request.args
    if args and args["room"]:
        asyncio.run_coroutine_threadsafe(move_to_room(args["room"]), DISCORD_ASYNCIO_LOOP)
        return "Moved to room!"
    
    return "No/wrong parameters given :( <br>Please use room?=[INSERT ROOM]"

@app.route('/setparty')
def api_setparty():
    """
        API endpoint for setting the current party.
        Should be used as:
            adress:port/setparty
    """

    asyncio.run_coroutine_threadsafe(set_party(), DISCORD_ASYNCIO_LOOP)
    return "Party set!"

# run flask app on main thread
app.run(host= '0.0.0.0', port=5335)




