import discord
import json
from discord.ext import commands

client = commands.Bot(command_prefix = '!')

token = open('file').read()

token = json.load(open('secrets.json', 'r'))['secret']

@client.event
async def on_ready():
    print("Bot is online! NO FREAKING WAY!!!! WHAT A BOSS LEO!!!!!")

client.run(token)