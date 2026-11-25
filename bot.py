"""
File: bot.py
Brief: Core code for the Bear Totem Companion bot
Author: Brandon Dennis
Version: 0.4
Last updated: 11/24/2026
TODO:
Implement error handler
"""

# base python imports
import asyncio
import os
import copy
import time
import discord

# discord.py specific imports
from discord import app_commands, Intents, CustomActivity, Interaction
from discord.app_commands import Choice
from discord.ext import commands
from discord.ext.commands.bot import _default
from discord.utils import MISSING
from dotenv import load_dotenv

# Other imports from the project folders
from HelperData.botHelper import *
from HelperData.exceptions import *
from HelperData.helpCommand import BTCHelp
from Objects.session import Session
from Objects.bracket import Bracket

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
DEV_ENV = os.getenv("DEV_GUILD")
DEV_GUILD, DEV_PERM, DEV_PUB_CHANNEL = DEV_ENV.split(",")
BT_ENV = os.getenv("BT_GUILD")
BT_GUILD, BT_PERM, BT_PUB_CHANNEL = BT_ENV.split(",")
# Test Variables
# """
TOKEN = os.getenv("TEST_TOKEN")
TEST_ENV = os.getenv("TEST_GUILD")
DEV_GUILD, DEV_PERM, DEV_PUB_CHANNEL = TEST_ENV.split(",")
# """
ENVIRONMENTS = {
    DEV_GUILD: [DEV_PERM, int(DEV_PUB_CHANNEL)],
    BT_GUILD: [BT_PERM, int(BT_PUB_CHANNEL)]
}

# Adds a session variable to the existing bot framework to use globally
class BTCBot(commands.Bot):
    def __init__(self, command_prefix, *, help_command = _default, tree_cls = app_commands.CommandTree, description = None, allowed_contexts = MISSING, allowed_installs = MISSING, intents, **options):
        super().__init__(command_prefix, help_command=help_command, tree_cls=tree_cls, description=description, allowed_contexts=allowed_contexts, allowed_installs=allowed_installs, intents=intents, **options)
        self.sessions:dict[str, Session] = {}
        self.environments = ENVIRONMENTS

intents = Intents.none()
intents.message_content = True
intents.messages = True
intents.guilds = True
btc = BTCBot(command_prefix="!", intents=intents, activity=CustomActivity(name="Type !help for the command menu."), help_command=BTCHelp())


async def bracket_autocomplete(inter: Interaction, current: str) -> list[Choice[int]]:
    bot: BTCBot = inter.client
    guild: str = inter.guild.name
    brackets: list[Bracket] = bot.sessions[guild].getBrackets()
    return [Choice(name=brackets[i].name, value=i + 1) for i in range(len(brackets))]


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

@btc.event
async def setup_hook():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await btc.load_extension(f"cogs.{filename[:-3]}")
            print(f"Loaded Cog: {filename[:-3]}")
        else:
            print("Unable to load pycache folder.")

@btc.check
async def permitCheck(ctx:commands.Context):
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


@btc.command(name="sync")
async def sync_command(ctx:commands.Context):
    if ctx.author.guild_permissions.administrator:
        btc.tree.copy_global_to(guild=ctx.guild)
        cmdList = await btc.tree.sync(guild=ctx.guild)
        await ctx.send(f"Synced {[cmd.name for cmd in cmdList]} commands to the server.")
    else:
        ctx.send("You do not have permission to use this command.")

# Login to Discord
async def login() -> None:
    async with btc:
        await btc.start(TOKEN)


# Don't run the login twice
if __name__ == "__main__":
    done = asyncio.run(login())
