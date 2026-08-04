# Main script for the John Doe bot
import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv
from botHelper import *

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

intents = discord.Intents.all()
intents.message_content = True
btc = commands.Bot(command_prefix="?", intents=intents)


@btc.command()
async def Help(ctx, cmd: str = ""):
    msg = ""
    if cmd:
        cmd = cmd.lower()
        if cmd in commandList:
            msg += f"{cmd.capitalize()}: {commandList[cmd]}\n"
        else:
            msg += f"Unknown command '{cmd}'. Please check the spelling of the command or use `?Help` to print a full list of commands"
    else:
        for key, val in commandList.items():
            msg += f"{key.capitalize()}: {val}\n"
    await ctx.send(msg[:-1])


@btc.command()
async def Doe(ctx, lv, classes="", reroll="true"):
    pass


@btc.event
async def on_error(event, *args, **kwargs):
    with open("err.log", "a") as f:
        if event == "on_message":
            f.write(f"Unhandled message: {args[0]}\n")
        else:
            raise


btc.run(TOKEN)
