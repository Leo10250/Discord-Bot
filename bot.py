import discord
import json
import random
from discord.ext import commands

client = commands.Bot(command_prefix = '!')

token = json.load(open('secrets.json', 'r'))['secret']

words = ["valorant",
        "alien isolation"]

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game("your feeling"))
    print("Bot is online!")

@client.event
async def on_member_join(member):
    print(f"{member}, please don't hurt me")

@client.event
async def on_member_remove(member):
    print(f"{member} is such a bruh")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if random.random() < 0.05:
        await message.channel.send(f"<@{message.author.id}> That's kinda gay")
        return

    if message.content.startswith("hello"):
        greetings = [f"<@{message.author.id}> It's me! The ruler of anime!",
                    f"<@{message.author.id}> As a weeb, I am so sorry for being alive",
                    f"<@{message.author.id}> Professional gamer here, welcome!"]
        if random.random() < 0.25:
            await message.channel.send(random.choice(greetings))
            return

    for i in words:
        if i in message.content.lower():
            if random.random() < 0.25:
                await message.channel.send(f"<@{message.author.id}> stfu")
                return

    if "among us" in message.content.lower():
        if random.random() < 0.25:
            await message.channel.send(f"<@{message.author.id}> you are getting vote off rn bro.")
            return

    await client.process_commands(message)

@client.command()
async def ping(ctx):
    response = [f"Shut the fuck up {round(client.latency * 1000)}ms boy",
                f"Here you go kind sir: {round(client.latency*1000)}ms",
                "No",
                "discord.errors.Forbidden: 403 Forbidden (error code: 50007): LEO TOLD ME TO NOT SEND MESSAGES TO THIS USER"]
    await ctx.send(random.choice(response))

@client.command(aliases = ["8ball"])
async def _8ball(ctx, *, question):
    answer = ["Idk",
            "www.google.com",
            "https://imgur.com/gallery/TCmi3"]
    await ctx.send(f"Question: {question}\nAnswer: {random.choice(answer)}")

@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

@client.command()
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)

@client.command()
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)

client.run(token)