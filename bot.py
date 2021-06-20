# Importing Discord API wrapper in Python
import discord
from discord.ext import commands

# Importing other libraries
import random
import string

# Prefix for command that are given to your discord bot
client = commands.Bot(command_prefix = '!')
print ("Assigning initial variables")
gamename_to_matches = {}

class Match:
  def __init__(self, gamename, id, player, numplayers):
    self.gamename = gamename
    self.id = id
    self.players = [player]
    self.numplayers = numplayers

#Sample user-defined function to call from event/command based functions
def hello_world():
    return "Hello World"

# Event based function - which tells when bot is online
@client.event
async def on_ready():
    # current_match_id = current_match_id
    # gamename_to_matches = gamename_to_matches
    print("Bot is available.")

# Defining functions that perform certain action for a command
# Function name should be same as the command followed by prefix
# Eg. !Hello , so function name should be Hello

# Sample command
# We'll leave this for the actual imp as it's pretty useful to check if server
# is live
@client.command()
async def Hello(ctx):
    ## ctx.send -- to send reply from bot to Discord server
    await ctx.send(f' Hello World')

@client.command()
# ctx is followed by parameters that are passed by user.
# For eg - !LFG AOE playername 4
async def LFG(ctx, gamename, player, numplayers):
    # Currently this logic might lead to collisions in IDs but we'll live with
    # it for now as it's incredibly unlikely with expected usage
    id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    await ctx.send(f' Creating request for Game : {gamename}. Looking for {numplayers} players. Group ID - {id}')

    if (gamename in gamename_to_matches):
      matches = gamename_to_matches[gamename]
    else:
      matches = {}
      gamename_to_matches[gamename] = matches
    matches[id] = Match(gamename, id, player, numplayers)
    await ctx.send(f'Active {gamename} games:-')
    for match_id in matches.keys():
      await ctx.send(f'{match_id}: {matches[match_id].players} {matches[match_id].numplayers}')

@client.command()
async def Join(ctx, id, player):
    print("Adding player {player} to match ({id})")
    await ctx.send(f'Player <member-name> added to GroupID {id} , Looking for <n-1> more player(s)')


@client.command()
async def Leave(ctx,id):
    print("Get member id and update to player list for Group ID {id}")
    await ctx.send(f'Player <member-name> removed from GroupID {id} , Looking for <n-1> more player(s)')


client.run('<insert token here>')
