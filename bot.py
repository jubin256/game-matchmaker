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
    global matches
    match_id = int(match_id)
    if match_id not in matches:
        await ctx.send(f'Match ID - {match_id} Not Found!')
        return
    else:
        print(f"Get member id and update to player list for Group ID {match_id}")
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
async def Purge(ctx, amount = 100):
    await ctx.channel.purge(limit=amount)

@client.command()
async def Help(ctx,*, command_name):
    await ctx.send(f'Welcome to Help Section')
    if command_name == 'LFG':
        await ctx.send(f'Usage: !LFG <gamename> <no.of.players>')
        await ctx.send(f'Purpose: Creates a New matchmaking request for a given game and required no. of players. Generates a unique match_id')
    elif command_name == 'Show':
        await ctx.send(f'Usage: !Show <gamename>')
        await ctx.send(f'Purpose: Displays all active matchmaking requests for a particular game')
    elif command_name == 'Join':
        await ctx.send(f'Usage: !Join <match_id>')
        await ctx.send(f'Purpose: Player can join matchmaking queue on mentioning the unique match_id')
    else:
        await ctx.send(f'Please choose one of the available commands.\nList of Available commands - "LFG","Show","Join"')

@client.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.CommandNotFound):
        await ctx.send(f'Oops! Command Not Found.\nPlease refer Help Section using command - !Help <command-name> to get detailed help for a certain command.\nList of Available commands - "LFG","Show","Join"')
    else:
        print(error)

client.run('NzUwMTg4MzU2MDc1NTIwMDYx.X025WQ.CB3g036hYTMjWYVhkEOrpue6e6c')
