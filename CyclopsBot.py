#!/usr/bin/env python

"""
The main code to be ran for CyclopsBot

Commented using reStructuredText (reST)

ToDo
    create and use a database for multiple servers
    server and clients where server responds saying the server is down if lost connection
"""
# Futures

# Built-in/Generic Imports
import os
import sys
import configparser
import shutil
import time

# Libs
import discord
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


# Checks for config file
if not os.path.exists("./configs/config.ini"):
    print("No config file can be found in ./configs/.")
    sys.exit("No config found.")
# Runs config file
config = configparser.ConfigParser()
try:
    config.read(os.path.abspath("./configs/config.ini"))
except FileNotFoundError:
    try:
        #shutil.copyfile("./configs/default_config.ini", "./configs/config.ini")
        print("You need to set up the config file correctly.")
    except shutil.Error:
        print("Something is wrong with the default config file or the config folder.")
        time.sleep(4)

    sys.exit()

# Constants
COGS_DIR = ".\cogs"
ADMIN_ROLE = config["Credentials"]["admin_role"]
BOT_TOKEN = config["Credentials"]["bot_token"]


os.system("title "+"Cyclops Bot")
client = commands.Bot(command_prefix=".")


@client.event
async def on_ready():
    """
    Ran after all cogs have been started and bot is ready
    :return:
    """
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="you sleep"))
    print("Bot is ready.")


@client.event
async def on_member_join(member):
    """
    When a member joins console will receive a notification
    :param member: Member that has joined
    :return:
    """
    print(member+" has joined the server")


@client.event
async def on_member_remove(member):
    """
    When a member is removed (kicked or left) console receives a notification
    :param member: Member that has left
    :return:
    """
    print(member+"has left the server")


@client.command()
async def ping(ctx):
    """
    Returns the ping of the bot
    :param ctx: Context of the command
    :return:
    """
    await ctx.send(f"Pong! {round(client.latency*1000)}ms")


#@client.command(aliases=['8ball','test'])
#async def _8ball(ctx, *, question):
#    ctx.send(f'Question = {question}')


@client.command()
@commands.has_role(ADMIN_ROLE)
async def clear(ctx, amount=2):
    """
    Clears a given number of messages from the given channel
    :param ctx: Context of the command
    :param amount: Amount of lines to delete
    :return:
    """
    await ctx.channel.purge(limit=amount)


@client.command()
@commands.has_role(ADMIN_ROLE)
async def load_cog(ctx, extension):
    """
    Loads a cog from the cogs folder
    :param ctx: Context of the command
    :param extension: The name of the cog
    :return:
    """
    client.load_extension(f'cogs.{extension}')


@client.command()
@commands.has_role(ADMIN_ROLE)
async def unload_cog(ctx, extension):
    """
    Unloads a running cog
    :param ctx: Context of the command
    :param extension: The name of the cog
    :return:
    """
    client.unload_extension(f'cogs.{extension}')




# Loads all cogs in COGS_DIR
for filename in os.listdir(COGS_DIR):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')




# Starts bot using the given BOT_ID
client.run(BOT_TOKEN)
