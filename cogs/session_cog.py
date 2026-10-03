"""
File: session_cog.py
Brief: Includes code for starting and stopping sessions
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
from Objects.session import Session
from bot import BTCBot

# Defines a cog for interacting with the entire session
class SessionCommands(commands.Cog):
    def __init__(self, bot:BTCBot):
        self.bot: BTCBot = bot

    # Starts a blank session using default value if none were given
    @commands.command(name="start")
    async def startSession(
        self,
        ctx: commands.Context,
        name: str = "Bear Totem Companion",
        tables: int | None = 7,
    ):
        # Make sure the number of tables can be converted to an integer
        try:
            tables = int(tables) if tables != None else 7
        except ValueError:
            await ctx.send(
                f"Invalid number_of_tables: '{tables}'. Please use a valid integer."
            )
            return

        # No session was found, create a session and give feedback
        if not self.bot.session:
            self.bot.session = Session(tables, name)
            await ctx.send(f"Created session with name: {self.bot.session.name}")
        # Current session found, send a feedback message
        else:
            await ctx.send(
                f"Session `{self.session.name}` already in progress. Please end the current session before starting a new one."
            )

    @commands.command(name="end")
    async def endSession(self, ctx: commands.Context):
        # Retrieve session variable and check for valid session.
        if self.bot.session:
            name = self.bot.session.name
            self.bot.session = None
            await ctx.send(f"Ended session '{name}'")
        else:
            await ctx.send("No current session found")


async def setup(client):
    await client.add_cog(SessionCommands(client))
