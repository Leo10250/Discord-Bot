#!/usr/bin/env python3
import discord
import json
import random
from discord.ext import commands, tasks
from itertools import cycle

client = commands.Bot(command_prefix = "!")
client.remove_command("help")

token = json.load(open("secrets.json", "r"))["secret"]

words = json.load(open("Arrays/forbidden_game_names.json", "r"))["game_names"]

websites = json.load(open("Arrays/links.json", "r"))["link"]

meter = json.load(open("Arrays/random_responses.json", "r"))["responses"]["random_response"]

greetings = json.load(open("Arrays/random_responses.json", "r"))["responses"]["random_greetings"]

status = cycle(json.load(open("Arrays/status_options.json", "r"))["playing"])

offend = json.load(open("Arrays/Insult.json", "r"))["bad"]

config = json.load(open('config.json', 'r'))

[
    DM_New_Member_Upon_Joining,
    Joining_Message,
    GIVE_ROLE_UPON_JOINING,
    role_ID,
    ALLOW_CUSTOM_MESSAGE,
    CUSTOM_MESSAGE_ON_MESSAGE,
    CUSTOM_MESSAGE_CHANCE
] = [config[i] for i in config]

CUSTOM_MESSAGE_CHANCE = int(CUSTOM_MESSAGE_CHANCE)

randMessage = 1

randReaction = 1

@client.event
async def on_ready():
    change_status.start()
    print("Bot is online!")

@client.event
async def on_member_join(member):

    # Auto adding roles upon joining
    if GIVE_ROLE_UPON_JOINING == True:
        role = discord.utils.get(member.server.roles, id=f"<{role_ID}>")
        await member.add_roles(member, role)

    # Dm new member upon joining
    if DM_New_Member_Upon_Joining == True:
        channel = await member.create_dm()
        await channel.send(Joining_Message)

    print(f"{member} has joined!")

@client.event
async def on_member_remove(member):
    print(f"{member} has left!")

last = 15343854848
last_web = 4138434834

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    elif message.channel.id == 753045768696234074:
        return

    global last
    global last_web
    if ALLOW_CUSTOM_MESSAGE == "True":
        print("true")
        if random.random() < CUSTOM_MESSAGE_CHANCE:
            print("method worked")
            current = random.randint(0, len(meter) - 1)
            while(last == current):
                current = random.randint(0, len(meter) - 1)
            last = current
            await message.channel.send(f"<@{message.author.id}> {CUSTOM_MESSAGE_ON_MESSAGE[current]}")
            return 

    if randMessage == 1:
        if random.random() < 0.01:
            if random.random() < 0.75:
                current = random.randint(0, len(meter) - 1)
                # global last
                while(last == current):
                    current = random.randint(0, len(meter) - 1)
                last = current
                await message.channel.send(f"<@{message.author.id}> {meter[current]}")
                return
            else:
                current_web = random.randint(0, len(websites) - 1)
                # global last_web
                while(last_web == current_web):
                    current_web = random.randint(0, len(websites) - 1)
                    last_web = current_web
                await message.channel.send(f"<@{message.author.id}> NO TIME TO EXPLAIN, WE GOTTA GO!\n{websites[current_web]}")
                return
    if randReaction == 1:
        if random.random() < 0.01:
            emoji = discord.utils.get(message.guild.emojis, name='pepePanties')
            if emoji:
                await message.add_reaction(emoji)
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
                "No"]
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
    await ctx.channel.purge(limit=1)
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

@client.command(pass_context=True)
async def dm(ctx, member : discord.Member, *, content):
    channel = await member.create_dm()
    await channel.send(f"**{ctx.message.author} said:** {content}")
    await ctx.channel.purge(limit=1)
    

@client.command(pass_context=True)
async def pm(ctx, member : discord.Member, *, content):
    channel1 = await member.create_dm()
    await channel1.send(f"{content}")
    await ctx.channel.purge(limit=1)

@client.command
async def randMessage_on(ctx):
    if ctx.message.author.guild_permissions.administrator:
        if(randMessage == 1):
            await ctx.send(f"<@{ctx.message.author.id}> Random_Message is already on...")
            return
        randMessage = 1
        await ctx.send(f"<@{ctx.message.author.id}> Random_Message is now on!")
    else:
        await ctx.send(f"<@{ctx.message.author.id}> You don't have the permission to enable Random_Message.")

# @randMessage_on.error
# async def enable_randMessage_error(ctx):
#     pass

@client.command
async def randMessage_off(ctx):
    if ctx.message.author.guild_permissions.administrator:
        if(randMessage == 0):
            await ctx.send(f"<@{ctx.message.author.id}> Random_Message is already off...")
            return
        randMessage = 0
        await ctx.send(f"<@{ctx.message.author.id}> Random_Message is now off!")
    else:
        await ctx.send(f"<@{ctx.message.author.id}> You don't have the permission to disable Random_Message.")  

# @randMessage_off.error
# async def disable_randMessage_error(ctx):
#     pass 

@client.command
async def randReact_on(ctx):
    if ctx.message.author.guild_permissions.administrator:
        if(randReaction == 1):
            await ctx.send(f"<@{ctx.message.author.id}> Random_Reaction is already on...")
            return
        randReaction = 1
        await ctx.send(f"<@{ctx.message.author.id}> Random_Reaction is now on!")
    else:
        await ctx.send(f"<@{ctx.message.author.id}> You don't have the permission to enable Random_Reaction.")

@client.command
async def randReact_off(ctx):
    if ctx.message.author.guild_permissions.administrator:
        if(randReaction == 0):
            await ctx.send(f"<@{ctx.message.author.id}> Random_Message is already off...")
            return
        randReaction = 0
        await ctx.send(f"<@{ctx.message.author.id}> Random_Message is now off!")
    else:
        await ctx.send(f"<@{ctx.message.author.id}> You don't have the permission to disable Random_Reaction.")  
    

@client.command()
async def help(ctx):
    embed = discord.Embed(colour = discord.Colour.orange())                             
    embed.set_author(name="Help")
    embed.add_field(name="!insult (user)", value="Insults designated member", inline=False)
    embed.add_field(name="!tell (*user*) [*message*]", value="@ and tells the designated member what you want it to say", inline=False)
    embed.add_field(name="!dm (*user*)[*message here]", value="Direct-messages a member of your choice(with name)", inline=False)
    embed.add_field(name="!pm (*user*) [*message here*]", value="Private-messages a member of your choice(no name)", inline=False)
    embed.add_field(name="!ping", value="Tells you your ping(most of the times)", inline=False)
    embed.add_field(name="!8ball *question here*", value="Answers your question", inline=False)
    embed.add_field(name="!clear", value="Clears a desginated number of messages", inline=False)
    embed.add_field(name="!kick *member*", value="Kicks a member(if with permission)", inline=False)
    embed.add_field(name="!ban *member*", value="Bans a member(if with permission)", inline=False)
    embed.add_field(name="!unban *member*", value="Unbans a member(if with permission)", inline=False)
    embed.add_field(name="!randMessage_on", value="allows the bot to send random messages", inline=False)
    embed.add_field(name="!randMessage_off", value="prevents the bot to send random messages", inline=False)
    embed.add_field(name="!randReact_on", value="allows the bot to randomly add a reaction to a message", inline=False)
    embed.add_field(name="!randReact_off", value="prevents the bot from randomly adding a reaction to a message", inline=False)
    embed.add_field(name="!help", value="Displays all available commands", inline=False)

    await ctx.send(embed=embed)

client.run(token)