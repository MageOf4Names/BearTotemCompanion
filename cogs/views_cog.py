"""
File: views_cog.py
Brief: Includes the code for commands that view the current bot session
Author: Brandon Dennis
Version: 0.4
Last updated: 11/13/2026
TODO:
Group commands
Implement auto complete and suggestions
"""

# discord.py specific imports
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands

# Other imports from the project folders
from HelperData.exceptions import *
from bot import BTCBot

bracket_options = [
    Choice(name="Play to Win", value=1),
    Choice(name="Super Casual", value=2),
    Choice(name="Play for Fun", value=3),
]

# Defines a cog for interacting with the entire session
class ViewSession(commands.Cog):
    def __init__(self, bot: BTCBot):
        self.bot: BTCBot = bot

    # Sends a message with the player count in one or all brackets
    @commands.hybrid_command(name="player-count")
    @app_commands.describe(bracket="Get a player count for a particular bracket")
    @app_commands.choices(bracket=bracket_options)
    async def playerCount(self, ctx: commands.Context, bracket: int | None = None):
        # Retrieve session variable and check for valid session.
        if await self.sessionNotFound(ctx): return
        session = self.bot.sessions[ctx.guild.name]
        # Error checking for non-integer bracket values
        try:
            bracket = int(bracket) if bracket else None
            if bracket == None:
                await ctx.send(session.playerCount())
            else:
                await ctx.send(session.playerCount(br=bracket - 1))
        except (ValueError, IndexError):
            await ctx.send(
                f"Invalid bracket: '{bracket}'. Please use a valid bracket index. Use !listBrackets to view the current brackets."
            )

    # Sends a message with a list of players in one or all brackets
    @commands.hybrid_command(name="player-list")
    @app_commands.describe(bracket="List players for a particular bracket")
    @app_commands.choices(bracket=bracket_options)
    async def playerList(self, ctx: commands.Context, bracket: int | None = None):
        # Retrieve session variable and check for valid session.
        if await self.sessionNotFound(ctx): return
        session = self.bot.sessions[ctx.guild.name]
        # Error checking for non-integer bracket values
        try:
            bracket = int(bracket) if bracket else None
            if bracket == None:
                await ctx.send(session.listPlayers())
            else:
                await ctx.send(session.listPlayers(br=bracket - 1))
        except (ValueError, IndexError):
            await ctx.send(
                f"Invalid bracket: '{bracket}'. Please use a valid bracket index. Use !listBrackets to view the current brackets."
            )

    # Sends a message with a list of players in one or all brackets
    @commands.hybrid_command(name="group-list")
    @app_commands.describe(bracket="List groups for a particular bracket")
    @app_commands.choices(bracket=bracket_options)
    async def groupList(
        self, 
        ctx: commands.Context,
        bracket: int | None = None,
    ):
        # Retrieve session variable and check for valid session.
        if await self.sessionNotFound(ctx): return
        session = self.bot.sessions[ctx.guild.name]
        # Error checking for non-integer bracket values
        try:
            bracket = int(bracket) if bracket else None
            if bracket == None:
                await ctx.send(session.listGroups())
            else:
                await ctx.send(session.listGroups(br=bracket - 1))
        except (ValueError, IndexError):
            await ctx.send(
                f"Invalid bracket: '{bracket}'. Please use a valid bracket index. Use !listBrackets to view the current brackets."
            )

    # Sends a message with all current brackets and their indexes
    @commands.hybrid_command(name="list-brackets")
    async def listBrackets(self, ctx: commands.Context):
        # Retrieve session variable and check for valid session.
        if await self.sessionNotFound(ctx): return
        await ctx.send(self.bot.sessions[ctx.guild.name].listBrackets)

    async def sessionNotFound(self, ctx: commands.Context):
        if ctx.guild.name not in self.bot.sessions:
            await ctx.send(
                "No current active session started. Use `!start` to start a default session or `!Help start` for more information"
            )
            return True
        return False


async def setup(client):
    await client.add_cog(ViewSession(client))
