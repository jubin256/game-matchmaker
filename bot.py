"""Bot which facilitates matchmaking on discord for arbitrary games."""

import random
import re
import string
import sys
import os

import discord
from discord.ext import commands

if __name__ == "__main__":
    try:
        auth_token = sys.argv[1]
    except IndexError:
        print("Usage: " + os.path.basename(__file__) + " <Auth Token>")
        sys.exit(1)

intents = discord.Intents.default()
intents.members = True  # Needed for on_reaction_remove
# Prefix for command that are given to your discord bot
client = commands.Bot(command_prefix='!', intents=intents)
print("Assigning initial variables...")
gamename_to_match_ids = {}
match_ids_to_matches = {}


class Match:
    """Data needed for a match to be played."""

    def __init__(self, gamename, id, player, numplayers):
        """Plain initializer."""
        self.gamename = gamename
        self.id = id
        self.players = {player}
        self.numplayers = numplayers


@client.event
async def on_ready():
    """Event based function - which tells when bot is online."""
    print("Bot is available.")

# Defining functions that perform certain action for a command
# Function name should be same as the command followed by prefix
# Eg. !Hello , so function name should be Hello


@client.command()
async def Hello(ctx):
    """Sample command: Useful to check if server is live."""
    await ctx.send('Hello World')


@client.command()
async def Help(ctx, *, command_name):
    """Give brief description of the command_name that is passed."""
    await ctx.send('Help')
    if command_name == 'LFG':
        await ctx.send('Usage: !LFG <gamename> <no.of.players>')
        await ctx.send(
            ("Purpose: Creates a new matchmaking request for a given game and "
                "required no. of players. Generates a unique match_id"))
    elif command_name == 'Show':
        await ctx.send('Usage: !Show <gamename>')
        await ctx.send(
            ("Purpose: Displays all active matchmaking requests for a "
                "particular game"))
    elif command_name == 'Join':
        await ctx.send('Usage: !Join <match_id>')
        await ctx.send(
            ("Purpose: Player can join matchmaking queue on mentioning the "
                "unique match_id"))
    else:
        await ctx.send(
            ("Please choose one of the available commands.\nList of Available "
                "commands - \"LFG\",\"Show\",\"Join\""))


@client.command()
async def LFG(ctx, gamename, player, numplayers):
    """Create a new matchmaking request for given game and required no. of players.

    For eg - !LFG AOE playername 4
    """
    if "_" in gamename:
        await ctx.send(
            f' Invalid game name: {gamename}. Should not have underscores')
        return
    # Currently this logic might lead to collisions in IDs but we'll live with
    # it for now as it's incredibly unlikely with expected usage
    random_postfix = "".join(
        random.choices(string.ascii_uppercase + string.digits, k=4))
    match_id = "_".join((gamename, random_postfix))
    await ctx.send(
        f' Creating request for Game : {gamename}.'
        f' Looking for {numplayers} players. Match ID - {match_id}'
        f' Thumbs up to this to join match - \"{match_id}\"')

    if gamename in gamename_to_match_ids:
        match_ids_of_game = gamename_to_match_ids[gamename]
    else:
        match_ids_of_game = set()
        gamename_to_match_ids[gamename] = match_ids_of_game
    match_ids_of_game.add(match_id)

    match_ids_to_matches[match_id] = \
        Match(gamename, match_id, player, int(numplayers))

    await ctx.send(f' Thumbs up to this to join match - \"{match_id}\"')
    await ctx.send(f'Active {gamename} games:-')
    for match_id in match_ids_of_game:
        match_of_game = match_ids_to_matches[match_id]
        await ctx.send(
            f'{match_id}: {match_of_game.players} {match_of_game.numplayers}')


@client.command()
async def Join(ctx, match_id, player):
    """Add player to matchmaking queue using the unique match_id."""
    await join_match(ctx, match_id, player)


@client.event
async def on_reaction_add(reaction, user):
    """Add user to matchmaking queue based on reaction.

    Use the unique match_id present in the message of the appropriate format
    and only if the reaction added is a thumbs up.
    """
    print('reaction added')
    message = reaction.message
    content = message.content
    if reaction.emoji == "👍" and "Thumbs up to this to join match" in content:
        matching = re.match(
            r'Thumbs up to this to join match - \"(.*)\"', content)
        match_id = matching.group(1)
        ctx = await client.get_context(message)
        await join_match(ctx, match_id, user.mention)


async def join_match(ctx, match_id, new_player):
    """Add player to matchmaking queue using the unique match_id."""
    gamename = match_id.split("_", 1)[0]
    print(
        f'Adding player {new_player} to match({match_id}) of game({gamename})')
    if gamename not in gamename_to_match_ids.keys():
        await ctx.send(f' Game \'{gamename}\' not found')
        return

    match_ids_of_game = gamename_to_match_ids[gamename]
    if match_id not in match_ids_of_game:
        print(f'Match ID \'{match_id}\' not found in {match_ids_of_game}')
        await ctx.send(f' Match ID \'{match_id}\' not found')
        return

    match = match_ids_to_matches[match_id]
    if len(match.players) >= match.numplayers:
        await ctx.send(f' Match ID \'{match_id}\' already full')
        return

    match.players.add(new_player)
    await ctx.send(f'Player {new_player} added to Match ID - {match_id}')

    if len(match.players) == match.numplayers:
        await ctx.send(
            f'Enough players for Match ID - {match_id}: {match.players}')
    else:
        num_players_left = match.numplayers - len(match.players)
        await ctx.send(f'Looking for {num_players_left} more player(s)')


@client.command()
async def Leave(ctx, match_id, player):
    """Remove player from matchmaking queue using the unique match_id."""
    await leave_match(ctx, match_id, player)


@client.event
async def on_reaction_remove(reaction, user):
    """Remove user from matchmaking queue based on reaction.

    Use the unique match_id present in the message of the appropriate format
    and only if the reaction being removed is a thumbs up.
    """
    print('reaction removed')
    message = reaction.message
    content = message.content
    if reaction.emoji == "👍" and "Thumbs up to this to join match" in content:
        matching = re.match(
            r'Thumbs up to this to join match - \"(.*)\"', content)
        match_id = matching.group(1)
        ctx = await client.get_context(message)
        await leave_match(ctx, match_id, user.mention)


async def leave_match(ctx, match_id, player):
    """Remove player from matchmaking queue using the unique match_id."""
    gamename = match_id.split("_", 1)[0]
    print(
        f'Removing player {player} from match({match_id}) of game({gamename})')
    if gamename not in gamename_to_match_ids.keys():
        await ctx.send(f' Game \'{gamename}\' not found')
        return

    match_ids_of_game = gamename_to_match_ids[gamename]
    if match_id not in match_ids_of_game:
        print(f'Match ID \'{match_id}\' not found in {match_ids_of_game}')
        await ctx.send(f' Match ID \'{match_id}\' not found')
        return

    match = match_ids_to_matches[match_id]

    match.players.remove(player)
    await ctx.send(f'Player {player} removed from Match ID - {match_id}')
    num_players_left = match.numplayers - len(match.players)
    await ctx.send(f'Looking for {num_players_left} player(s)')

print(f'Using auth token:"{auth_token}" to connect...')
client.run(auth_token)
