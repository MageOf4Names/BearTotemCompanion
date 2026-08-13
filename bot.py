"""
File: bot.py
Brief: Core code for the Bear Totem Companion bot
Author: Brandon Dennis
Version: 0.1.0
Last updated: 8/13/2026
TODO:
- Guard against exceptions for all commands
"""

# Main script for the Bear Totem Companion bot
import os
import copy

import discord
from discord.ext import commands
from dotenv import load_dotenv

from HelperData.botHelper import *
from HelperData.exceptions import *
from Objects.session import Session

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

intents = discord.Intents.none()
intents.message_content = True
intents.messages = True
btc = commands.Bot(command_prefix="!", intents=intents, activity=discord.CustomActivity(name="Type !Help for the command menu."))
session:Session = None


@btc.command()
async def Help(ctx, cmd: str=""):
    msg = ""
    if cmd:
        cmd = cmd.lower()
        found = False
        for key, val in commandList.items():
            if cmd == key.lower():
                msg += f"{key}: {val}"
        if not found:
            msg += f"Unknown command '{cmd}'. Please check the spelling of the command or use `?Help` to print a full list of commands"
        await ctx.send(msg)
    else:
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
async def start(ctx, tables:int=7, name:str="Bear Totem Commander Night"):
    global session
    if not session:
        session = Session(tables, name)
        await ctx.send(f"Created session with name: {name}")
    else:
        await ctx.send(f"Session `{session.name}` already in progress. Please end the current session before starting a new one.")

@btc.command()
async def add(ctx, bracket, name:str):
    global session
    if session == None:
        await ctx.send("No current active session started. Use `!start` to start a default session or `!Help start` for more information")
        return

    # Error checking for existing players and non-integer brackets
    try:
        bracket = int(bracket)
        session.addPlayer(bracket - 1, name)
        await ctx.send(f"Player added to bracket {session.getBracket(bracket - 1)}")
    except PlayerExistsError as error:
        await ctx.send(error)
    except (ValueError, IndexError):
        await ctx.send(f"Invalid bracket: '{bracket}'. Please use a valid bracket index. Use !listBrackets to view the current brackets.")

@btc.command()
async def addBulk(ctx, bracket, *args):
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
async def remove(ctx, player:str):
    global session
    if session == None:
        await ctx.send("No current active session started. Use `!start` to start a default session or `!Help start` for more information")
        return

    try:
        session.removePlayer(player)
        await ctx.send(f"Player {player} removed from the session.")
    except PlayerNotFound as error:
        await ctx.send(error)

@btc.command()
async def changeBracket(ctx, bracket:int, player:str):
    global session
    if session == None:
        await ctx.send("No current active session started. Use `!start` to start a default session or `!Help start` for more information")
        return
    # Error checking for non-integer bracket values
    try:
        bracket = int(bracket)
        session.changeBracket(bracket - 1, player)
        await ctx.send(f"Changed player {player} to bracket {session.getBracket(bracket - 1)}")
    except (ValueError, IndexError):
        await ctx.send(f"Invalid bracket: '{bracket}'. Please use a valid bracket index. Use !listBrackets to view the current brackets.")
    except PlayerExistsError:
        await ctx.send(f"Player {player} is already in bracket {session.getBracket(bracket - 1)}")

@btc.command()
async def group(ctx, bracket, *args):
    global session
    if session == None:
        await ctx.send("No current active session started. Use `!start` to start a default session or `!Help start` for more information")
        return
    # Error checking for non-integer bracket values
    try:
        bracket = int(bracket)
        session.makeGroup(bracket - 1, args)
        await ctx.send(f"Created a group of {len(args)} players in bracket {session.getBracket(bracket - 1)}")
    except (ValueError, IndexError):
        await ctx.send(f"Invalid bracket: '{bracket}'. Please use a valid bracket index. Use !listBrackets to view the current brackets.")
    except PlayerAlreadyGroupedError as error:
        await ctx.send(error)

@btc.command()
async def playerCount(ctx, bracket=None):
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
async def listPlayers(ctx, bracket=None):
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
async def listBrackets(ctx):
    global session
    if session == None:
        await ctx.send("No current active session started. Use `!start` to start a default session or `!Help start` for more information")
        return
    await ctx.send(session.listBrackets)

@btc.command()
async def startRound(ctx):
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
    global session
    if session:
        name = session.name
        session = None
        await ctx.send(f"Ended session '{name}'")

@btc.event
async def on_error(event, *args, **kwargs):
    with open("err.log", "a") as f:
        if event == "on_message":
            f.write(f"Unhandled message: {args[0]}\n")
        else:
            raise


btc.run(TOKEN)
