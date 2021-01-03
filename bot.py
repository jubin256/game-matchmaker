# Importing Discord API wrapper in Python
import discord
from discord.ext import commands

# Importing other libraries
import random
import string

# Prefix for command that are given to your discord bot
client = commands.Bot(command_prefix = '!')
print ("Assigning initial variables")
line_break = "------------------------------------------------------"
gamename_to_matches = {}


class Match:
  def __init__(self, gamename, match_id, player, numplayers):
    self.gamename = gamename
    self.id = match_id
    self.players = [player]
    self.numplayers = numplayers

# Event based function - which tells when bot is online
@client.event
async def on_ready():
    print("Bot is available.")

@client.command()
# Command to create Matchmaking request. Usage - !LFG AOE playername 4
async def LFG(ctx, gamename, numplayers):
    match_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    player = ctx.message.author.mention
    await ctx.send(f' Creating request for Game : {gamename}. Looking for {numplayers} players. Group ID - {match_id}')

    if (gamename in gamename_to_matches):
        matches = gamename_to_matches[gamename]
    else:
        matches = {}
        gamename_to_matches[gamename] = matches
    matches[match_id] = Match(gamename, match_id, player, numplayers)
    await ctx.send('Matchmaking Request Created')
    await ctx.send(f' Match ID : {match_id} No. of Players - {matches[match_id].numplayers}')
    await ctx.send('Players -')
    for player in matches[match_id].players :
        await ctx.send(f'{player}')
      

@client.command()
# Command to show all active matchmaking requests for a particular game. Usage - !Show AOE
async def Show(ctx, gamename):
    if (gamename in gamename_to_matches):
        matches = gamename_to_matches[gamename]
        await ctx.send(f'Active {gamename} games:-')
        for match_id in matches.keys():
            await ctx.send(f' Match ID : {match_id} No. of Players - {matches[match_id].numplayers}')
            await ctx.send('Players -')
            for player in matches[match_id].players :
                await ctx.send(f'{player}')
            await ctx.send(f'{line_break}')
    else:
        await ctx.send(f'No Existing matchmaking request for game: {gamename}. Create new request using command - !LFG <game-name> <no-of-players>')

@client.command()
async def Join(ctx,gamename,match_id):
    print(f"Get member id and update to player list for Group ID {match_id}")
    if (gamename in gamename_to_matches):
        matches = gamename_to_matches[gamename]
        players = matches[match_id].players
        numplayers = int(matches[match_id].numplayers)
        if len(players) < numplayers:
            if ctx.message.author.mention not in matches[match_id].players:
                matches[match_id].players.append(ctx.message.author.mention)
            else:
                #matches[match_id].players.append("temp-testing")
                await ctx.send(f'Player already in queue for Match ID: {match_id}')
                return
            await ctx.send(f'Gamename - {gamename} Match ID : {match_id} No. of Players - {matches[match_id].numplayers}')
            await ctx.send('Players -')
            for player in matches[match_id].players :
                await ctx.send(f'{player}')
            await ctx.send(f'{line_break}')
            if len(players) == numplayers:
                print('*** Player Queue is full for Match ID: {match_id}. Remove from Active matchmaking requests. ***')
                await ctx.send('Matchmaking Completed! Enjoy your Game!')
                ## Remove from active matchmaking request dict ---write code here---
        else:
            await ctx.send(f'Player Queue Full for Match ID: {match_id}')




@client.command()
async def Leave(ctx,match_id):
    print(f"Get member id and update to player list for Group ID {match_id}")
    await ctx.send(f'Player <member-name> removed from GroupID {match_id} , Looking for <n-1> more player(s)')

@client.command()
async def Purge(ctx, amount = 10):
    await ctx.channel.purge(limit=amount)


client.run('NzUwMTg4MzU2MDc1NTIwMDYx.X025WQ.CB3g036hYTMjWYVhkEOrpue6e6c')
