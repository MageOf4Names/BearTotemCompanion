"""
File: edits_cog.py
Brief: Includes code for commands that directly edit the session
Author: Brandon Dennis
Version: 0.2
Last updated: 10/2/2026
TODO:
Group commands
Implement auto complete and suggestions
"""

# general imports
import copy

# discord.py specific imports
from discord.ext import commands

# Other imports from the project folders
from HelperData.exceptions import *
from bot import BTCBot


# Defines a cog for interacting with the entire session
class EditSession(commands.Cog):
    def __init__(self, bot: BTCBot):
        self.bot: BTCBot = bot

    # Adds a player to a specified bracket
    @commands.command(name="add")
    async def addPlayer(self, ctx: commands.Context, bracket, name: str):
        # Retrieve session variable and check for valid session.
        if await self.sessionNotFound(ctx): return

        # Error checking for existing players and non-integer brackets
        try:
            bracket = int(bracket)
            self.bot.session.addPlayer(bracket - 1, name)
            await ctx.send(f"Player added to bracket {self.bot.session.getBracket(bracket - 1)}")
        # Handle errors gracefully
        except PlayerExistsError as error:
            await ctx.send(error)
        except (ValueError, IndexError):
            await ctx.send(
                f"Invalid bracket: '{bracket}'. Please use a valid bracket index. Use !listBrackets to view the current brackets."
            )

    # Adds a list of players in bulk to a specified bracket.
    @commands.command(name="addBulk")
    async def bulkAddPlayer(self, ctx: commands.Context, bracket, *args):
        # Retrieve session variable and check for valid session.
        if await self.sessionNotFound(ctx): return
        # Error checking for non-integer bracket values
        try:
            bracket = int(bracket)
        except (ValueError, IndexError):
            await ctx.send(
                f"Invalid bracket: '{bracket}'. Please use a valid bracket index. Use !listBrackets to view the current brackets."
            )
            return

        dupes = ""
        added = 0
        for player in args:
            # Add each player, or note the name if the player is already found in the bracket
            try:
                self.bot.session.addPlayer(bracket - 1, player)
                added += 1
            except PlayerExistsError:
                dupes += f"{player}, "
        # Create the appropriate feedback message.
        msg = f"Added {added} players to bracket {self.bot.session.getBracket(bracket - 1)}"
        if dupes != "":
            msg += (
                f"\nThe following players were already found in this bracket: {dupes[:-2]}"
            )
        await ctx.send(msg)

    # Removes a player with a given name from the session
    @commands.command(name="remove")
    async def removePlayer(self, ctx: commands.Context, player: str):
        # Retrieve session variable and check for valid session.
        if await self.sessionNotFound(ctx): return

        # Try to remove player or send feedback if they don't exist
        try:
            self.bot.session.removePlayer(player)
            await ctx.send(f"Player {player} removed from the session.")
        except PlayerNotFound as error:
            await ctx.send(error)

    # Changes the bracket of a player to the specified bracket
    @commands.command(name="changeBracket")
    async def changePlayerBracket(self, ctx: commands.Context, bracket: int, player: str):
        # Retrieve session variable and check for valid session.
        if await self.sessionNotFound(ctx): return
        # Error checking for non-integer bracket values and redundant changes
        try:
            bracket = int(bracket)
            self.bot.session.changeBracket(bracket - 1, player)
            await ctx.send(
                f"Changed player {player} to bracket {self.bot.session.getBracket(bracket - 1)}"
            )
        # Handle errors gracefully
        except (ValueError, IndexError):
            await ctx.send(
                f"Invalid bracket: '{bracket}'. Please use a valid bracket index. Use !listBrackets to view the current brackets."
            )
        except PlayerExistsError:
            await ctx.send(
                f"Player {player} is already in bracket {self.bot.session.getBracket(bracket - 1)}"
            )

    # Creates a group of players in a given bracket
    @commands.command(name="group")
    async def groupPlayers(
        self,
        ctx: commands.Context,
        bracket,
        *args,
    ):
        # Retrieve session variable and check for valid session.
        if await self.sessionNotFound(ctx): return
        # Error checking for non-integer bracket values and players in existing groups
        try:
            bracket = int(bracket)
            self.bot.session.makeGroup(bracket - 1, args)
            await ctx.send(
                f"Created a group of {len(args)} players in bracket {self.bot.session.getBracket(bracket - 1)}"
            )
        # Handle errors gracefully
        except (ValueError, IndexError):
            await ctx.send(
                f"Invalid bracket: '{bracket}'. Please use a valid bracket index. Use !listBrackets to view the current brackets."
            )
        except PlayerAlreadyGroupedError as error:
            await ctx.send(error)

    # Starts a round and seats all players in all brackets
    @commands.command(name="startRound")
    async def startRound(self, ctx: commands.Context):
        # Retrieve session variable and check for valid session.
        if await self.sessionNotFound(ctx): return

        # Create a copy of the session in case startup encounters an error
        backup = copy.deepcopy(self.bot.session)
        try:
            out = self.bot.session.startRound()
            self.bot.session.setDownstairs(0, False)
            # If the envoronment has a public channel configured, send to that
            public = (
                self.bot.get_channel(self.bot.environments[ctx.guild.name][1])
                if ctx.guild.name in self.bot.environments
                else ctx
            )
            for msg in out:
                await public.send(msg)
        except UnderfullBracketError as error:
            # If the round start fails, revert to the backup session
            self.bot.session = backup
            await ctx.send(error)

    async def sessionNotFound(self, ctx):
        if not self.bot.session:
            await ctx.send(
                "No current active session started. Use `!start` to start a default session or `!Help start` for more information"
            )
            return True
        return False


async def setup(client):
    await client.add_cog(EditSession(client))
