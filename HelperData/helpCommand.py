"""
File: helpCommand.py
Brief: A child class of discord.ext.commands.HelpCommand used in the Bear Totem Companion bot
Author: Brandon Dennis
Version: 0.2
Last updated: 10/2/2026
TODO:
"""

import discord as ds
from discord.ext import commands
from HelperData.botHelper import commandList as cl

class BTCHelp(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        # Continously generate the help message
        msg = "# Help Menu:\n"
        # `mapping` is a dict of the bot's cogs, which map to their commands
        for cog, cmds in mapping.items():  # get the cog and its commands separately
            # Set the cog name, or 'Ungrouped' if there is none
            msg += "Ungrouped:\n" if cog == None else f"{cog.qualified_name}:\n"
            msg += "```"
            # Pre-process the command list to find the proper padding length
            padding_len = 0
            raw = {}
            for c in cmds:
                # Add commands to the raw dict and find the max length for padding
                if len(c.name) > padding_len: padding_len = len(c.name)
                raw[c.name] = cl[c.name].brief if c.name in cl else ""
            # Add the commands to the end message using the proper padding
            for name, desc in raw.items():
                msg += f"\t{name}{" " * (padding_len - len(name))} | {desc}\n"
            msg += "```\n"
        # Additional help info
        msg += "Type `!help [command]` to get detailed use information on a specific command"
        channel = self.get_destination()  # this method is inherited from `HelpCommand`, and gets the channel in context
        await channel.send(msg)

    async def send_command_help(self, command:commands.Command):
        name = command.name
        msg = f"## Command: {name}\nFunction: {cl[name].description}\nUsage:\n\t`!{name} "
        if cl[name].parameters:
            params = {}
            padding = 0
            # Go through each parameter and add it to the usage line while adding it to a string message for later
            for key, p in cl[name].parameters.items():
                # Give the parameter square braces if it's required
                if p.require:
                    p_name = key
                    msg += f"[{key}] "
                # Otherwise, curly braces and add "(optional)" to the parameter name
                else:
                    p_name = key + " (optional)"
                    msg += "{" + key + "} "
                # Assign the label to the name and add the default value to it if there is one
                params[p_name] = p.label
                if not p.require and p.default != None:
                    params[p_name] += f" (default value: {p.default})"
                # Find the max length parameter name for padding
                if len(p_name) > padding:
                    padding = len(p_name)
            msg = msg[:-1]
            msg += "`\nParameters:\n```"
            for key, val in params.items():
                msg += f"{key}{" " * (padding - len(key))} | {val}\n"
            msg += "```"
        else:
            msg += "`"
                
        channel = self.get_destination()  # this method is inherited from `HelpCommand`, and gets the channel in context
        await channel.send(msg)

    async def send_cog_help(self, cog):
        return await super().send_cog_help(cog)

    async def send_group_help(self, group):
        return await super().send_group_help(group)

    async def send_error_message(self, error):
        return await super().send_error_message(error)
