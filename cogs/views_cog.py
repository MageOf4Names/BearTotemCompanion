"""
File: views_cog.py
Brief: Includes the code for commands that view the current bot session
Author: Brandon Dennis
Version: 0.2
Last updated: 10/2/2026
TODO:
Group commands
Implement auto complete and suggestions
"""

# discord.py specific imports
from discord.ext import commands

# Other imports from the project folders
from HelperData.exceptions import *
from bot import BTCBot


# Defines a cog for interacting with the entire session
class ViewSession(commands.Cog):
    def __init__(self, bot: BTCBot):
        self.bot: BTCBot = bot

    # Sends a message with the player count in one or all brackets
    @commands.command(name="playerCount")
    async def playerCount(self, ctx: commands.Context, bracket: int | None = None):
        # Retrieve session variable and check for valid session.
        if await self.sessionNotFound(ctx): return
        # Error checking for non-integer bracket values
        try:
            bracket = int(bracket) if bracket else None
            if bracket == None:
                await ctx.send(self.bot.session.playerCount())
            else:
                await ctx.send(self.bot.session.playerCount(br=bracket - 1))
        except (ValueError, IndexError):
            await ctx.send(
                f"Invalid bracket: '{bracket}'. Please use a valid bracket index. Use !listBrackets to view the current brackets."
            )

    # Sends a message with a list of players in one or all brackets
    @commands.command(name="playerList")
    async def playerList(self, ctx: commands.Context, bracket: int | None = None):
        # Retrieve session variable and check for valid session.
        if await self.sessionNotFound(ctx): return
        # Error checking for non-integer bracket values
        try:
            bracket = int(bracket) if bracket else None
            if bracket == None:
                await ctx.send(self.bot.session.listPlayers())
            else:
                await ctx.send(self.bot.session.listPlayers(br=bracket - 1))
        except (ValueError, IndexError):
            await ctx.send(
                f"Invalid bracket: '{bracket}'. Please use a valid bracket index. Use !listBrackets to view the current brackets."
            )

    # Sends a message with a list of players in one or all brackets
    @commands.command(name="groupList")
    async def groupList(
        self, 
        ctx: commands.Context,
        bracket: int | None = None,
    ):
        # Retrieve session variable and check for valid session.
        if await self.sessionNotFound(ctx): return
        # Error checking for non-integer bracket values
        try:
            bracket = int(bracket) if bracket else None
            if bracket == None:
                await ctx.send(self.bot.session.listGroups())
            else:
                await ctx.send(self.bot.session.listGroups(br=bracket - 1))
        except (ValueError, IndexError):
            await ctx.send(
                f"Invalid bracket: '{bracket}'. Please use a valid bracket index. Use !listBrackets to view the current brackets."
            )

    # Sends a message with all current brackets and their indexes
    @commands.command(name="listBrackets")
    async def listBrackets(self, ctx: commands.Context):
        # Retrieve session variable and check for valid session.
        if await self.sessionNotFound(ctx): return
        await ctx.send(self.bot.session.listBrackets)

    async def sessionNotFound(self, ctx):
        if not self.bot.session:
            await ctx.send(
                "No current active session started. Use `!start` to start a default session or `!Help start` for more information"
            )
            return True
        return False


async def setup(client):
    await client.add_cog(ViewSession(client))
