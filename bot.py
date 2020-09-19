import discord
import json
import random
from discord.ext import commands

client = commands.Bot(command_prefix = "!")

token = json.load(open("secrets.json", "r"))["secret"]

words = json.load(open("Arrays/forbidden_game_names.json", "r"))["game_names"]

websites = json.load(open("Arrays/links.json", "r"))["link"]

meter = json.load(open("Arrays/random_responses.json", "r"))["responses"]["random_response"]

greetings = json.load(open("Arrays/random_responses.json", "r"))["responses"]["random_greetings"]

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game("your feeling"))
    print("Bot is online!")

@client.event
async def on_member_join(member):
    print(f"{member} has joined!")

@client.event
async def on_member_remove(member):
    print(f"{member} has left!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if random.random() < 0.01:
        if random.random() < 0.75:
            await message.channel.send(f"<@{message.author.id}> {random.choice(meter)}")
            return
        else:
            await message.channel.send(f"<@{message.author.id}> NO TIME TO EXPLAIN, WE GOTTA GO!\n{random.choice(websites)}")
            return
    
    if "gay" in message.content.lower():
        if random.random() < 0.2:
            await message.channel.send(f"<@{message.author.id}> Leo, is that you?")

    if message.content.startswith("hello"):
        if random.random() < 0.25:
            await message.channel.send(f"<@{message.author.id}> {random.choice(greetings)}")
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
    await ctx.send(f"Kicked {member.mention}\nreason: {reason}")

@client.command()
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"Banned {member.mention}\nreason: {reason}")

@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if(user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"Unbanned {user.mention}")
            return

client.run(token)