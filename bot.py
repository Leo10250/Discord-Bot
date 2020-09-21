#!/usr/bin/env python3
import discord
import json
import random
from discord.ext import commands, tasks
from itertools import cycle

client = commands.Bot(command_prefix = "!")

token = json.load(open("secrets.json", "r"))["secret"]

words = json.load(open("Arrays/forbidden_game_names.json", "r"))["game_names"]

websites = json.load(open("Arrays/links.json", "r"))["link"]

meter = json.load(open("Arrays/random_responses.json", "r"))["responses"]["random_response"]

greetings = json.load(open("Arrays/random_responses.json", "r"))["responses"]["random_greetings"]

status = cycle(json.load(open("Arrays/status_options.json", "r"))["playing"])

offend = json.load(open("Arrays/Insult.json", "r"))["bad"]

@client.event
async def on_ready():
    change_status.start()
    print("Bot is online!")

@client.event
async def on_member_join(member):
    # Auto adding roles upon joining
    #  
    # role = discord.utils.get(ctx.guild.roles, name = "{whatever your role is}") 
    # await ctx.add_roles(role)

    print(f"{member} has joined!")

@client.event
async def on_member_remove(member):
    print(f"{member} has left!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if random.random() < 0.01:
        emoji = discord.utils.get(message.guild.emojis, name='pepePanties')
        if emoji:
            await message.add_reaction(emoji)
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
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"<@{ctx.message.author.id}> You do not have the permission to edit messages.")

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"Kicked {member.mention}\nreason: {reason}")

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"<@{ctx.message.author.id}> You do not have the permission to kick members.")

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"Banned {member.mention}\nreason: {reason}")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"<@{ctx.message.author.id}> You do not have the permission to ban members.")

@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if(user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"Unbanned {user.mention}")
            return

@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"<@{ctx.message.author.id}> You do not have the permission to unban members.")

@client.command()
async def tell(ctx, member : discord.Member, *, reason):
    await ctx.send(f"{member.mention} {reason}")

@tell.error
async def tell_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
        await ctx.send(f"<@{ctx.message.author.id}> Bruh, you are using this command wrong...\nExample:\nInput: !tell <@{ctx.message.author.id}> You did something wrong!\nOutput: <@{ctx.message.author.id}> You did something wrong!")

@client.command()
async def insult(ctx, member : discord.Member):
    if member.id == 578715287491182595:
        if random.random() < 0.5:
            await ctx.send(f"<@{ctx.message.author.id}> HOW DARE YOU INSULT MY MASTER!!!\n{member.mention} My lord, what should I do with this big bruh?")
            return
    await ctx.send(f"{member.mention} {random.choice(offend)}")

@insult.error
async def insult_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
        await ctx.send(f"<@{ctx.message.author.id}> You can't even insult people correctly?\nHere is how:\n !insult <@{ctx.message.author.id}> {random.choice(offend)}")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"<@{ctx.message.author.id}> That is not a valid command for me!\nUse !help to check out all existing commands!\nB r u h")

@tasks.loop(hours=10)
async def change_status():
    await client.change_presence(status=discord.Status.online, activity=discord.Game(next(status)))

def obtain_id(ctx):
    return ctx.author.id

def is_it_me(ctx):
    return obtain_id == 578715287491182595

client.run(token)