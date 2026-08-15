"""
File: bot.py
Brief: Core code for the Bear Totem Companion bot
Author: Brandon Dennis
Version: 0.1.0
Last updated: 8/14/2026
TODO:
"""

# Main script for the Bear Totem Companion bot
import os
import copy
import time

import discord
from discord.ext import commands
from dotenv import load_dotenv

from HelperData.botHelper import *
from HelperData.exceptions import *
from Objects.session import Session

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
DEV_ENV = os.getenv("DEV_GUILD")
DEV_GUILD, DEV_PERM = DEV_ENV.split(",")
BT_ENV = os.getenv("BT_GUILD")
BT_GUILD, BT_PERM = BT_ENV.split(",")

intents = discord.Intents.none()
intents.message_content = True
intents.messages = True
intents.guilds = True
btc = commands.Bot(command_prefix="!", intents=intents, activity=discord.CustomActivity(name="Type !Help for the command menu."))
session:Session = None


@btc.command()
# Brings up a help menu for a specific command, or all commands if none is specified
async def Help(ctx, cmd: str=""):
    # Check the incoming guild and permissions to see if the user is permitted to use commands.
    if not await permitCheck(ctx): return
    # Empty message variable to make sending messages easier
    msg = ""
    # If a command was given, search through command list to see if it is valid.
    if cmd:
        cmd = cmd.lower()
        found = False
        # Compare the given command against all known commands
        for key, val in commandList.items():
            # If found, set message and the found flag
            if cmd == key.lower():
                msg += f"{key}: {val}"
                found = True
        # If the command isn't found, set msg to a helper message
        if not found:
            msg += f"Unknown command '{cmd}'. Please check the spelling of the command or use `?Help` to print a full list of commands"
        # Send the intended message
        await ctx.send(msg)
    else:
        # Go through each command and add it to msg until it hits the character limit
        for key, val in commandList.items():
            tmp = f"{key}: {val}\n\n"
            # Make sure the message is under the character limit.
            if len(msg) + len(tmp) < 2000:
                msg += tmp
            # Otherwise, send the message and reset msg.
            else:
                await ctx.send(msg)
                msg = f"\n{tmp}"
        await ctx.send(msg)


@btc.command()
# Starts a blank session using default value if none were given
async def start(ctx, tables: int = 7, name: str = "Bear Totem Commander Night"):
    # Check the incoming guild and permissions to see if the user is permitted to use commands.
    if not await permitCheck(ctx): return
    global session
    # No session was found, create a session and give feedback
    if not session:
        session = Session(tables, name)
        await ctx.send(f"Created session with name: {name}")
    # Current session found, send a feedback message
    else:
        await ctx.send(f"Session `{session.name}` already in progress. Please end the current session before starting a new one.")


@btc.command()
# Adds a player to a specified bracket
async def add(ctx, bracket, name: str):
    # Check the incoming guild and permissions to see if the user is permitted to use commands.
    if not await permitCheck(ctx): return
    # Retrieve session variable and check for valid session.
    global session
    if session == None:
        await ctx.send("No current active session started. Use `!start` to start a default session or `!Help start` for more information")
        return

    # Error checking for existing players and non-integer brackets
    try:
        bracket = int(bracket)
        session.addPlayer(bracket - 1, name)
        await ctx.send(f"Player added to bracket {session.getBracket(bracket - 1)}")
    # Handle errors gracefully
    except PlayerExistsError as error:
        await ctx.send(error)
    except (ValueError, IndexError):
        await ctx.send(f"Invalid bracket: '{bracket}'. Please use a valid bracket index. Use !listBrackets to view the current brackets.")


@btc.command()
# Adds a list of players in bulk to a specified bracket.
async def addBulk(ctx, bracket, *args):
    # Check the incoming guild and permissions to see if the user is permitted to use commands.
    if not await permitCheck(ctx): return
    # Retrieve session variable and check for valid session.
    global session
    if session == None:
        await ctx.send("No current active session started. Use `!start` to start a default session or `!Help start` for more information")
        return
    # Error checking for non-integer bracket values
    try:
        bracket = int(bracket)
    except (ValueError, IndexError):
        await ctx.send(f"Invalid bracket: '{bracket}'. Please use a valid bracket index. Use !listBrackets to view the current brackets.")
        return

    dupes = ""
    added = 0
    for player in args:
        # Add each player, or note the name if the player is already found in the bracket
        try:
            session.addPlayer(bracket - 1, player)
            added += 1
        except PlayerExistsError:
            dupes += f"{player}, "
    # Create the appropriate feedback message.
    msg = f"Added {added} players to bracket {session.getBracket(bracket - 1)}"
    if dupes != "":
        msg += f"\nThe following players were already found in this bracket: {dupes[:-2]}"
    await ctx.send(msg)


@btc.command()
# Removes a player with a given name from the session
async def remove(ctx, player: str):
    # Check the incoming guild and permissions to see if the user is permitted to use commands.
    if not await permitCheck(ctx): return
    # Retrieve session variable and check for valid session.
    global session
    if session == None:
        await ctx.send("No current active session started. Use `!start` to start a default session or `!Help start` for more information")
        return

    # Try to remove player or send feedback if they don't exist
    try:
        session.removePlayer(player)
        await ctx.send(f"Player {player} removed from the session.")
    except PlayerNotFound as error:
        await ctx.send(error)


@btc.command()
# Changes the bracket of a player to the specified bracket
async def changeBracket(ctx, bracket: int, player: str):
    # Check the incoming guild and permissions to see if the user is permitted to use commands.
    if not await permitCheck(ctx): return
    # Retrieve session variable and check for valid session.
    global session
    if session == None:
        await ctx.send("No current active session started. Use `!start` to start a default session or `!Help start` for more information")
        return
    # Error checking for non-integer bracket values and redundant changes
    try:
        bracket = int(bracket)
        session.changeBracket(bracket - 1, player)
        await ctx.send(f"Changed player {player} to bracket {session.getBracket(bracket - 1)}")
    # Handle errors gracefully
    except (ValueError, IndexError):
        await ctx.send(f"Invalid bracket: '{bracket}'. Please use a valid bracket index. Use !listBrackets to view the current brackets.")
    except PlayerExistsError:
        await ctx.send(f"Player {player} is already in bracket {session.getBracket(bracket - 1)}")


@btc.command()
# Creates a group of players in a given bracket
async def group(ctx, bracket, *args):
    # Check the incoming guild and permissions to see if the user is permitted to use commands.
    if not await permitCheck(ctx): return
    # Retrieve session variable and check for valid session.
    global session
    if session == None:
        await ctx.send("No current active session started. Use `!start` to start a default session or `!Help start` for more information")
        return
    # Error checking for non-integer bracket values and players in existing groups
    try:
        bracket = int(bracket)
        session.makeGroup(bracket - 1, args)
        await ctx.send(f"Created a group of {len(args)} players in bracket {session.getBracket(bracket - 1)}")
    # Handle errors gracefully
    except (ValueError, IndexError):
        await ctx.send(f"Invalid bracket: '{bracket}'. Please use a valid bracket index. Use !listBrackets to view the current brackets.")
    except PlayerAlreadyGroupedError as error:
        await ctx.send(error)


@btc.command()
# Sends a message with the player count in one or all brackets
async def playerCount(ctx, bracket=None):
    # Check the incoming guild and permissions to see if the user is permitted to use commands.
    if not await permitCheck(ctx): return
    # Retrieve session variable and check for valid session.
    global session
    if session == None:
        await ctx.send("No current active session started. Use `!start` to start a default session or `!Help start` for more information")
        return
    # Error checking for non-integer bracket values
    try:
        bracket = int(bracket) if bracket else None
        if bracket == None:
            await ctx.send(session.playerCount())
        else:
            await ctx.send(session.playerCount(br=bracket - 1))
    except (ValueError, IndexError):
        await ctx.send(f"Invalid bracket: '{bracket}'. Please use a valid bracket index. Use !listBrackets to view the current brackets.")


@btc.command()
# Sends a message with a list of players in one or all brackets
async def listPlayers(ctx, bracket=None):
    # Check the incoming guild and permissions to see if the user is permitted to use commands.
    if not await permitCheck(ctx): return
    # Retrieve session variable and check for valid session.
    global session
    if session == None:
        await ctx.send("No current active session started. Use `!start` to start a default session or `!Help start` for more information")
        return
    # Error checking for non-integer bracket values
    try:
        bracket = int(bracket) if bracket else None
        if bracket == None:
            await ctx.send(session.listPlayers())
        else:
            await ctx.send(session.listPlayers(br=bracket - 1))
    except (ValueError, IndexError):
        await ctx.send(f"Invalid bracket: '{bracket}'. Please use a valid bracket index. Use !listBrackets to view the current brackets.")


@btc.command()
# Sends a message with all current brackets and their indexes
async def listBrackets(ctx):
    # Check the incoming guild and permissions to see if the user is permitted to use commands.
    if not await permitCheck(ctx): return
    # Retrieve session variable and check for valid session.
    global session
    if session == None:
        await ctx.send("No current active session started. Use `!start` to start a default session or `!Help start` for more information")
        return
    await ctx.send(session.listBrackets)


@btc.command()
# Starts a round and seats all players in all brackets
async def startRound(ctx):
    # Check the incoming guild and permissions to see if the user is permitted to use commands.
    if not await permitCheck(ctx): return
    # Retrieve session variable and check for valid session.
    global session
    if session == None:
        await ctx.send("No current active session started. Use `!start` to start a default session or `!Help start` for more information")
        return

    # Create a copy of the session in case startup encounters an error
    backup = copy.deepcopy(session)
    try:
        out = session.startRound()
        session.setDownstairs(0, False)
        for msg in out:
            await ctx.send(msg)
    except UnderfullBracketError as error:
        # If the round start fails, revert to the backup session
        session = backup
        await ctx.send(error)


@btc.command()
async def end(ctx):
    # Check the incoming guild and permissions to see if the user is permitted to use commands.
    if not await permitCheck(ctx): return
    # Retrieve session variable and check for valid session.S
    global session
    if session:
        name = session.name
        session = None
        await ctx.send(f"Ended session '{name}'")


@btc.command()
async def check(ctx):
    print(ctx.permissions.administrator)


@btc.event
async def on_error(event, *args, **kwargs):
    with open("err.log", "a") as f:
        if event == "on_message":
            f.write(f"Unhandled message: {args[0]}\n")
        else:
            raise

@btc.event
async def on_ready():
    print(f"{btc.user} is connected to the following guilds:")
    for guild in btc.guilds:
        print(f"{guild.name}(id: {guild.id})")


async def permitCheck(ctx:commands.Context):
    print(ctx.guild.name)
    if ctx.guild.name == BT_GUILD:
        permit = False
        match BT_PERM:
            case "admin":
                permit = ctx.permissions.administrator
            case _:
                pass
    elif ctx.guild.name == DEV_GUILD:
        # Test value for checking permission issues
        # permit = False
        permit = True
    else:
        permit = True
    if not permit:
        await ctx.send("Looks like you don't have permission to use me here!")
    return permit


btc.run(TOKEN)
