import discord
from discord.ext import commands

client = commands.Bot(command_prefix = '!')

@client.event
async def on_ready():
    print("Bot is online! NO FREAKING WAY!!!! WHAT A BOSS LEO!!!!!")

client.run("NzU2MjA4OTU0MDMxMzQxNjg4.X2OgeA.0ycQgEghBKNd4UMnklcA3luBebY")