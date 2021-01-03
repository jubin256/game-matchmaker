# Importing Discord API wrapper in Python
import discord
from discord.ext import commands

# Importing other libraries
import random
import string

# Prefix for command that are given to your discord bot
client = commands.Bot(command_prefix = '!')
counter = 0
line_break = "------------------------------------------------------"
matches = {} ## {match_id : MatchObject}


class Match:
  def __init__(self, gamename, player, numplayers):
    self.gamename = gamename
    self.players = [player]
    self.numplayers = numplayers

# Event based function - which tells when bot is online
@client.event
async def on_ready():
    print("Bot is available.")

@client.command()
# Command to create Matchmaking request. Usage - !LFG AOE playername 4
async def LFG(ctx, gamename, numplayers):
    global counter
    counter = counter+1
    match_id = counter
    player = ctx.message.author.mention
    matches[match_id] = Match(gamename, player, numplayers)       
    await ctx.send(f'Matchmaking Request Created\nGame - **{gamename}** \nMatch ID : **{match_id}** \nLooking for **{matches[match_id].numplayers} Players** \nPlayers in Queue -')
    for player in matches[match_id].players :
        await ctx.send(f'{player}')
      

@client.command()
# Command to show all active matchmaking requests for a particular game. Usage - !Show AOE
async def Show(ctx, gamename):
    await ctx.send(f'Active {gamename} games:-')
    match_found = False
    for match_id in matches:
        if matches[match_id].gamename == gamename:
            match_found = True
            players_str = ", ".join(matches[match_id].players)
            await ctx.send(f'\nMatch ID : **{match_id}** \nLooking for **{matches[match_id].numplayers} Players** \nPlayers in Queue - {players_str}\n{line_break}')                  
    if match_found == False:
        await ctx.send(f'No Existing matchmaking request for game: {gamename}. Create new request using command - !LFG <game-name> <no-of-players>')

@client.command()
async def Join(ctx,match_id):
    print(f"Get member id and update to player list for Group ID {match_id}")
    global matches
    match_id = int(match_id)
    players = matches[match_id].players
    gamename = matches[match_id].gamename
    numplayers = int(matches[match_id].numplayers)
    if len(players) < numplayers:
        if ctx.message.author.mention not in matches[match_id].players:
            matches[match_id].players.append(ctx.message.author.mention)
        else:
            #matches[match_id].players.append("temp-testing")
            await ctx.send(f'Player already in queue for Match ID: {match_id}')
            return
        players_str = ", ".join(matches[match_id].players)
        await ctx.send(f'Gamename - **{gamename}**\nMatch ID : **{match_id}** \nLooking for **{matches[match_id].numplayers} Players** \nPlayers in Queue - {players_str}\n{line_break}')
        if len(players) == numplayers:
            print(f'*** Player Queue is full for Match ID: {match_id}. Remove from Active matchmaking requests. ***')
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
