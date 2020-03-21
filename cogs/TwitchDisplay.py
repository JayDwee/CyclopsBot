#!/usr/bin/env python

"""
This is a Cog used to display live twitch broadcasts to a discord text channel

Commented using reStructuredText (reST)

https://curl.trillworks.com/#python used to learn requests

ToDo

"""
# Futures

# Built-in/Generic Imports
import os
import sys
import configparser
import shutil
import time
import codecs
import sqlite3

# Libs
import discord
import requests
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
CONFIG_PATH = "./configs/config.ini"
DEFAULT_EMBED = discord.Embed(
            title=":desktop: Program Status",
            colour=discord.Colour.blue()
        )


# Checks for config file
if not os.path.exists("./configs/config.ini"):
    print("No config file can be found in ./configs/.")
    sys.exit("No config found.")
# Runs config file
config = configparser.ConfigParser()
try:
    # config.read(os.path.abspath("./configs/config.ini"))
    config.read_file(codecs.open(CONFIG_PATH, "r", "utf-8-sig"))
except FileNotFoundError:
    try:
        # shutil.copyfile("./configs/default_config.ini", "./configs/config.ini")
        print("You need to set up the config file correctly.")
    except shutil.Error:
        print("Something is wrong with the default config file or the config folder.")
        time.sleep(4)
    sys.exit()

# Config Constants
ADMIN_ROLE = config["Credentials"]["admin_role"]
CLIENT_ID = config["TwitchDisplay"]["client_id"]
HEADERS = {'Client-ID': CLIENT_ID, }


class TwitchDisplay(commands.cog):
    """
    The Cog for Twitch Display
    """

    def __init__(self, client):
        """
        :param client: the bot client parsed in from the main program
        """
        self.started = False
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

        if not self.started:
            self.find_processes.start(msg)
            started = True
        print("TwitchDisplay Running")


    def update_twitch_team_live(team_name):
        users = requests.get('https://api.twitch.tv/kraken/teams/'+team_name, headers=HEADERS).json().get("users")

        while len(users) != 0:
            url = 'https://api.twitch.tv/helix/streams?'
            users_left = 100
            for user_info in users:
                url += "user_login=" + user_info.get("name")+"&"
                users.remove(user_info)
                if users_left == 1:
                    break
                else:
                    users_left -= 1
            url = url[:-1]
            user_streams = requests.get(url, headers=HEADERS).json().get("data")

            for user in user_streams:
                if user.get('type') == "live":
                    print(user.get("user_name") + "is streaming at https://twitch.tv/"+user.get("user_name").lower())

    update_twitch_team_live("uosvge")