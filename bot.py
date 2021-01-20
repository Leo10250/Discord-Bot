#!/usr/bin/env python3
import discord
import json
import random
from discord.ext import commands, tasks
from discord.utils import find
from itertools import cycle
from requests import get
from udpy import UrbanClient


def get_prefix(client, message):
    with open("Arrays/prefixes.json", "r") as f:
        prefixes = json.load(f)
    
    return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix = get_prefix)
client.remove_command("help")

token = json.load(open("secrets.json", "r"))["secret"]

words = json.load(open("Arrays/forbidden_game_names.json", "r"))["game_names"]

websites = json.load(open("Arrays/links.json", "r"))["link"]

meter = json.load(open("Arrays/random_responses.json", "r"))["responses"]["random_response"]

greetings = json.load(open("Arrays/random_responses.json", "r"))["responses"]["random_greetings"]

activity = cycle(json.load(open("Arrays/status_options.json", "r"))["activity"])

status = cycle(json.load(open("Arrays/status_options.json", "r"))["status"])

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

LEVEL_SYSTEM = 1

@client.event
async def on_ready():
    print("Bot is online!")
    change_status.start()

@client.event
async def on_guild_join(guild):
    with open("Arrays/prefixes.json", "r") as f:
        prefixes = json.load(f)
    
    prefixes[str(guild.id)] = "!"

    with open("Arrays/prefixes.json" , "w") as f:
        json.dump(prefixes, f, indent=4)

    general = find(lambda x: x.name == 'general',  guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        await general.send("https://i.pinimg.com/564x/37/ab/89/37ab89389766b74058bc5b38c2edc4b6.jpg")
        await general.send('DAFAQ? \nUse !help to learn more. \nUse !change_prefix to do the you know what ;)')

@client.event
async def on_guild_remove(guild):
    with open("Arrays/prefixes.json", "r") as f:
        prefixes = json.load(f)
    
    prefixes.pop(str(guild.id))

    with open("Arrays/prefixes.json" , "w") as f:
        json.dump(prefixes, f, indent=4)



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

    # if LEVEL_SYSTEM == 1: 
    #     users = json.load(open("Arrays/users.json", "r"))

    #     await update_data(users, member)

    #     json.dump(users, open("Arrays/users.json", "w"), indent=4)

    # print(f"{member} has joined!")

@client.event
async def on_member_remove(member):
    # print(f"{member} has left!")
    ...

last = 15343854848
last_web = 4138434834

@client.event
async def on_message(message):
    if not "!" in message.content.lower():
        if message.author.bot:
            return
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

        #  BROKEN LEVEL SYSTEM

        # if LEVEL_SYSTEM == 1:
        #     users = json.load(open("Arrays/users.json", "r"))

        #     await update_data(users, message.author)
        #     await add_experience(users, message.author, 5)
        #     await level_up(users, message.author, message.channel)

        #     json.dump(users, open("Arrays/users.json", "w"), indent=4)


        if randMessage == 1:
            random_num = random.random() 
            if random_num < 0.0001:
                current = random.randint(0, len(meter) - 1)
                # global last
                while(last == current):
                    current = random.randint(0, len(meter) - 1)
                last = current
                await message.channel.send(f"<@{message.author.id}> {meter[current]}")
                return
            elif random_num >= 0.0001 and random_num < 0.0002:
                current_web = random.randint(0, len(websites) - 1)
                # global last_web
                while(last_web == current_web):
                    current_web = random.randint(0, len(websites) - 1)
                    last_web = current_web
                await message.channel.send(f"<@{message.author.id}> NO TIME TO EXPLAIN, WE GOTTA GO!\n{websites[current_web]}")
                return
            # elif random_num >= 0.001 and random_num < 0.0015:
            #     await message.channel.send("https://i.chzbgr.com/full/8091158016/h223D6252/sigh-here-we-go-again")
            # elif random_num >= 0.0015 and random_num < 0.002:
            #     await message.channel.send("https://i.kym-cdn.com/photos/images/original/001/398/111/d5a")
            # elif random_num >= 0.002 and random_num < 0.0025:
            #     await message.channel.send("https://memegenerator.net/img/instances/58910158.jpg")

        if randReaction == 1:
            if random.random() < 0.01:
                emoji = discord.utils.get(message.guild.emojis, name='pepePanties')
                if emoji:
                    await message.add_reaction(emoji)
                    return
        
        # if "wait it" in message.content.lower():
        #     await message.channel.send(f"<@{message.author.id}> Shhhhhhhh \nhttps://i.redd.it/spoaltgn8ud51.jpg")

        if "gay" in message.content.lower():
            if random.random() < 0.05:
                await message.channel.send(f"<@{message.author.id}> Leo, is that you?")

        if message.content.startswith("hello"):
            if random.random() < 0.25:
                await message.channel.send(f"<@{message.author.id}> {random.choice(greetings)}")
                return

        for i in words:
            if i in message.content.lower():
                if random.random() < 0.01:
                    await message.channel.send(f"<@{message.author.id}> stfu")
                    return

        if "among us" in message.content.lower():
            if random.random() < 0.01:
                await message.channel.send(f"<@{message.author.id}> you are getting voted off rn bro.")
                return

    await client.process_commands(message)

@client.command()
async def getprefix(ctx):
    with open("Arrays/prefixes.json", "r") as f:
        prefixes = json.load(f)
    
    await ctx.send(prefixes[str(ctx.guild.id)])

@client.command()
async def change_prefix(ctx, prefix):
    if ctx.message.author.guild_permissions.administrator:
        prefixes = json.load(open("Arrays/prefixes.json", "r"))
        #default prefix
        prefixes[str(ctx.guild.id)] = prefix

        with open("Arrays/prefixes.json" , "w") as f:
            json.dump(prefixes, f, indent=4)

        await ctx.send(f"The new prefix is now {prefix}")

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
            "https://imgur.com/gallery/TCmi3",
            "Yes!"]
    await ctx.send(f"Question: {question}\nAnswer: {random.choice(answer)}")

@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount+1)

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"<@{ctx.message.author.id}> You do not have the permission to edit messages.")

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    if member.id == 578715287491182595:
        await ctx.send(f"<@{ctx.message.author.id}> HOW DARE YOU INSULT MY MASTER!!!\n{member.mention} My lord, what should I do with this big bruh?")
        return
    if member.id == 756208954031341688:
        await ctx.send(f"<@{ctx.message.author.id}> You do not have the permission to kick **ME**.")
        return
    await member.kick(reason=reason)
    await ctx.send(f"Kicked {member.mention}\nreason: {reason}")

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"<@{ctx.message.author.id}> You do not have the permission to kick members.")

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    if member.id == 578715287491182595:
        await ctx.send(f"<@{ctx.message.author.id}> HOW DARE YOU INSULT MY MASTER!!!\n{member.mention} My lord, what should I do with this big bruh?")
        return
    if member.id == 756208954031341688:
        await ctx.send(f"<@{ctx.message.author.id}> You do not have the permission to ban **ME**.")
        return
    await member.ban(reason=reason)
    await ctx.send(f"Banned {member.mention}\nreason: {reason}")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"<@{ctx.message.author.id}> You do not have the permission to ban members.")

@client.command()
async def video(ctx):
    current_web = random.randint(0, len(websites) - 1)
    global last_web
    while(last_web == current_web):
        current_web = random.randint(0, len(websites) - 1)
        last_web = current_web
    await ctx.send(f"{websites[current_web]}")

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
async def say(ctx, *, reason):
    await ctx.channel.purge(limit=1)
    await ctx.send(f"{reason}")

@client.command()
async def unzip(ctx):
    await ctx.channel.purge(limit=1)
    await ctx.send("https://i.chzbgr.com/full/8091158016/h223D6252/sigh-here-we-go-again")

@client.command()
async def perhaps(ctx):
    await ctx.channel.purge(limit=1)
    await ctx.send("https://i.kym-cdn.com/photos/images/original/001/398/111/d5a")


@tell.error
async def say_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
        await ctx.send(f"<@{ctx.message.author.id}> Bruh, you are using this command wrong...\nExample:\nInput: !say You did something wrong!\nOutput: You did something wrong!")

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

@client.command(pass_context=True)
async def meme(ctx):
    headers = {'User-Agent': 'Calm Leo Bot Version 1.0'}
    num = random.random()
    if(num <= 0.3):
        memes = json.load(open("Arrays/memes.json", "r"))["memes"]
        await ctx.send(random.choice(memes))
    elif(num > 0.3 and num <= 0.6): 
        i = 0
        error = 1
        while(error != 0):
        #print(f"https://www.reddit.com/r/{names}/random.json")
            try:
                reddit_post = get(f"https://www.reddit.com/r/memes/random.json", headers = headers).json()
                await ctx.send(reddit_post[0]['data']['children'][0]['data']['url'])
                error = 0
            except:
                error = 1
                if(i >= 5):
                    #print("end")
                    await ctx.send(f"Hmmmm. Something went wrong)\n-brought to you by this command has failed **{i}** times gang")
                    return
                i = i + 1
                #print(f"Wrong\n {i}")
        #print("sent")
    else:
        i = 0
        error = 1
        #print(f"https://www.reddit.com/r/{names}/random.json")
        while(error != 0):
            try:
                reddit_post = get(f"https://www.reddit.com/r/dankmemes/random.json", headers = headers).json()
                await ctx.send(reddit_post[0]['data']['children'][0]['data']['url'])
                error = 0
            except:
                error = 1
                if(i >= 5):
                    #print("end")
                    await ctx.send(f"Hmmmm. Something went wrong)\n-brought to you by this command has failed **{i}** times gang")
                    return
                i = i + 1
                #print(f"Wrong\n {i}")
            #print("sent")

@client.command(pass_context=True)
async def quote(ctx):
    quotes = json.load(open("Arrays/quotes.json", "r"))["quote"]
    embed = discord.Embed(colour = random.randint(0, 0xffffff))
    embed.add_field(name="Quote", value=f"\n{random.choice(quotes)}", inline=False)
    await ctx.send(embed=embed)

@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game(next(activity)))

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
async def waifu(ctx):
    headers = {'User-Agent': 'Calm Leo Bot Version 1.0'}
    i = 0
    error = 1
    while(error != 0):
        try:
            reddit_post = get('https://www.reddit.com/r/animegirls/random.json', headers = headers).json()
            await ctx.send(reddit_post[0]['data']['children'][0]['data']['url'])
            error = 0
        except:
            error = 1
            if(i >= 5):
                #print("end")
                await ctx.send(f"Hmmmm. Something went wrong)\n-brought to you by this command has failed **{i}** times gang")
                return
            i = i + 1
            #print("Wrong")


@client.command()
async def reddit(ctx, *, name):
    headers = {'User-Agent': 'Calm Leo Bot Version 1.0'}
    names = name.replace(" ", "")
    i = 0
    error = 1
    #print(f"https://www.reddit.com/r/{names}/random.json")
    while(error != 0):
        try:
            reddit_post = get(f"https://www.reddit.com/r/{names}/random.json", headers = headers).json()
            await ctx.send(reddit_post[0]['data']['children'][0]['data']['url'])
            error = 0
        except:
            error = 1
            if(i >= 5):
                #print("end")
                await ctx.send(f"Either this subreddit doesn't exist or I am too dumb.\nIt's probably the latter ;)\n-brought to you by this command has failed **{i}** times gang")
                return
            i = i + 1
            #print(f"Wrong\n {i}")
    #print("sent")

@client.command()
async def youtube(ctx):
    headers = {'User-Agent': 'Calm Leo Bot Version 1.0'}
    i = 0
    error = 1
    #print(f"https://www.reddit.com/r/{names}/random.json")
    while(error != 0):
        try:
            reddit_post = get(f"https://www.reddit.com/r/deepintoyoutube/random.json", headers = headers).json()
            await ctx.send(reddit_post[0]['data']['children'][0]['data']['url'])
            error = 0
        except:
            error = 1
            if(i >= 5):
                #print("end")
                await ctx.send(f"Either this subreddit doesn't exist or I am too dumb.\nIt's probably the latter ;)\n-brought to you by this command has failed **{i}** times gang")
                return
            i = i + 1
            #print(f"Wrong\n {i}")
    #print("sent")

@client.command()
async def ud(ctx, *, term):
    clients = UrbanClient()
    defs = clients.get_definition(term)
    i = -1
    j = -1
    temp = 0
    try:
        for d in defs:
            i += 1
            if(d.upvotes > temp):
                j = i
                temp = d.upvotes

        i = 0
        for d in defs:
            if(i == j):
                embed = discord.Embed(colour = discord.Colour.green())
                embed.set_footer(text=f"{d.upvotes} upvotes")
                # embed.set_author(name=f"{term}")                             
                embed.add_field(name=f"{term.upper()}", value=f"{d.definition}", inline=True)
                await ctx.send(embed=embed)
                return
            i = i + 1

        #error handling
        embed = discord.Embed(colour = discord.Colour.green())
        embed.set_footer(text=f"Something went wrong and I am extremely sorry\n┬─┬ ノ( ゜-゜ノ)")                         
        embed.add_field(name=f"I DON'T FUCKING KNOW!", value=f"Go google it yourself you lazy piece of bruh\n(╯°□°）╯︵ ┻━┻", inline=True)
        await ctx.send(embed=embed)

    except:
        embed = discord.Embed(colour = discord.Colour.green())
        embed.set_footer(text=f"Something went wrong and I am extremely sorry\n┬─┬ ノ( ゜-゜ノ)")                        
        embed.add_field(name=f"I DON'T FUCKING KNOW!", value=f"Go google it yourself you lazy piece of bruh\n(╯°□°）╯︵ ┻━┻", inline=True)
        await ctx.send(embed=embed)

    
@client.command()
async def help(ctx):
    embed = discord.Embed(colour = discord.Colour.orange())                             
    embed.set_author(name="Calm Leo", icon_url = "https://i.pinimg.com/originals/8f/90/39/8f90394879fd28a09e09bf4faf7ee017.jpg")
    # embed.set_thumbnail(url="https://i.pinimg.com/originals/8f/90/39/8f90394879fd28a09e09bf4faf7ee017.jpg")
    # embed.set_image(url="https://i.pinimg.com/originals/8f/90/39/8f90394879fd28a09e09bf4faf7ee017.jpg")
    embed.add_field(name="!change_prefix [*prefix*]", value="Change the prefix", inline=True)
    embed.add_field(name="!reddit [*subreddit name*]", value="Image from that subreddit", inline=True)
    embed.add_field(name="!ud (*word*)", value="Looks up the word on urban dictionary", inline=True)
    embed.add_field(name="!waifu", value="WAIFU", inline=True)
    embed.add_field(name="!meme", value="Displays a meme", inline=True)
    embed.add_field(name="!video", value="Quality meme videos", inline=True)
    embed.add_field(name="!youtube", value="Random YouTube videos", inline=True)
    embed.add_field(name="!insult (*user*)", value="Insults designated member", inline=True)
    embed.add_field(name="!tell (*user*) [*message*]", value="@ and sends the designated member the message", inline=True)
    embed.add_field(name="!say [*message*]", value="bot sends the designated message", inline=True)
    embed.add_field(name="!unzip", value="PLEASE DON'T USE IT", inline=True)
    embed.add_field(name="!perhaps", value="PLEASE DON'T USE IT EITHER", inline=True)
    embed.add_field(name="!dm (*user*)[*message here]", value="Direct-messages a member of your choice(with name)", inline=True)
    embed.add_field(name="!pm (*user*) [*message here*]", value="Private-messages a member of your choice(no name)", inline=True)
    embed.add_field(name="!ping", value="Tells you your ping(most of the times)", inline=True)
    embed.add_field(name="!8ball *question here*", value="Answers your question", inline=True)
    embed.add_field(name="!help", value="Displays all available commands", inline=True)
    embed.add_field(name="!modhelp", value="Displays all available commands for moderators", inline=True)
    embed.add_field(name="!devhelp", value="Displays all available commands for developers", inline=True)

    await ctx.send(embed=embed)

@client.command()
async def modhelp(ctx):
    embed = discord.Embed(colour = discord.Colour.red()) 
    embed.add_field(name="!clear", value="Clears a desginated number of messages", inline=True)
    embed.add_field(name="!kick *member*", value="Kicks a member(if with permission)", inline=True)
    embed.add_field(name="!ban *member*", value="Bans a member(if with permission)", inline=True)
    embed.add_field(name="!unban *member*", value="Unbans a member(if with permission)", inline=True)

    await ctx.send(embed=embed)



@client.command()
async def devhelp(ctx):
    embed = discord.Embed(colour = discord.Colour.blue()) 
    embed.add_field(name="!change_prefix [*prefix*]", value="Change the prefix", inline=True)
    embed.add_field(name="!getprefix", value="displays the prefix", inline=True)                            
    embed.add_field(name="!randMessage_on", value="allows the bot to send random messages", inline=True)
    embed.add_field(name="!randMessage_off", value="prevents the bot to send random messages", inline=True)
    embed.add_field(name="!randReact_on", value="allows the bot to randomly add a reaction to a message", inline=True)
    embed.add_field(name="!randReact_off", value="prevents the bot from randomly adding a reaction to a message", inline=True)

    await ctx.send(embed=embed)


client.run(token)