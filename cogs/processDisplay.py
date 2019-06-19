#!/usr/bin/env python

"""
This is a Cog used to display processes/ programs running on the client to a discord text channel

Commented using reStructuredText (reST)

ToDo
    create and use a database for multiple servers
"""
# Futures

# Built-in/Generic Imports

# Libs
import discord
import psutil
from discord.ext import commands, tasks

# Own modules

__author__ = "Jack Draper"
__copyright__ = "Unofficial Copyright 2019, CyclopsBot"
__credits__ = ["Jack Draper"]
__license__ = "Developer"
__version__ = "0.0.1"
__maintainer__ = "Jack Draper"
__email__ = "thejaydwee@gmail.com"
__status__ = "Development"
# "Prototype", "Development", or "Production"

# Constants
ADMIN_ROLE = 'Founders'
TEXT_CHANNEL = 590459824437985300
processes = {"cmd.exe": "Command Prompt", "chrome.exe": "Chrome", "Discord.exe": "Discord", "Steam.exe": "Steam"}


class ProcessDisplay(commands.Cog):
    """
    The Cog for Process Display
    """

    def __init__(self, client):
        """
        :param client: the bot client parsed in from the main program
        """
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        """
        Ran when bot is starting up and ready
        Deletes messages from the bot in the TEXTCHANNEL
        starts up find_processes method
        :return:
        """
        channel = self.client.get_channel(TEXT_CHANNEL)

        msg = await self.delete_bot_msg(channel)
        print(msg)
        self.find_processes.start(msg)
        print("Bot online2")

    # Commands
    @commands.command()
    @commands.has_role(ADMIN_ROLE)
    async def add_process(self, ctx, process, name):
        """
        Adds a process to the process display.
        Must be different from ones currently displayed.

        :param ctx: Context of the command
        :param process: The process (e.g. 'cmd.exe') to be added
        :param name: The name to be displayed for the process (e.g. 'Command Prompt')
        :return:
        """
        if process in processes.keys():
            await ctx.send(f"The process {process} is already being displayed")

        elif name in processes.values():
            await ctx.send(f"The process name {name} is already being displayed")

        else:
            processes[process] = name

    @commands.command()
    @commands.has_role(ADMIN_ROLE)
    async def remove_process(self, ctx, name):
        """
        Removes a process from the process display

        :param ctx: Context of the command
        :param name: Name displayed for the process (e.g. Command Prompt)
        :return:
        """
        for process in processes.keys():
            if processes.get(process) == name:
                processes.pop(process)

    @tasks.loop(seconds=1)
    async def find_processes(self, msg):
        """
        The processes with statuses are attached to the msg given

        :param msg: The message to be edited with the processes
        :return:
        """
        running_processes = []
        new_embed = discord.Embed(
            title=":desktop: Program Status",
            colour=discord.Colour.blue()
        )

        for proc in psutil.process_iter():
            if proc.name() in processes.keys():
                running_processes.append(proc.name())

        for process in processes:
            if process in running_processes:
                new_embed.add_field(name=processes.get(process), value="Online :white_check_mark:")
            else:
                new_embed.add_field(name=processes.get(process), value="Offline <:red_cross:590500648639004673>")

        await msg.edit(content="", embed=new_embed)


    def is_me(self, m):
        """
        Checks if a messages author is the bot
        :param m: tbh idk, maybe message?
        :return:
        """
        return m.author == self.client.user

    async def delete_bot_msg(self, channel):
        """
        Deletes up to the last 100 messages sent by the bot in the given channel
        :param channel: The channel that will have the messages deleted
        :return: the message that says how many messages were deleted
        """
        deleted = await channel.purge(limit=100, check=self.is_me)
        return await channel.send('Deleted {} message(s)'.format(len(deleted)))


def setup(client):
    """
    Ran on setup of the Cog
    :param client: The bot client
    :return:
    """
    client.add_cog(ProcessDisplay(client))
