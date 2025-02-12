#!/usr/bin/env python3
import asyncio
from NHentai.entities.doujin import DoujinThumbnail
import discord
import json
import random
from discord import Member
from discord.ext import commands, tasks
from discord.utils import find
from itertools import cycle
from requests import get
from udpy import UrbanClient
import os
from NHentai import NHentai
import re
import time
from datetime import datetime
import googleapiclient.discovery
from urllib.parse import parse_qs, urlparse

intents = discord.Intents.default()
intents.members = True
slientMember = False
sliencedMember = 1
counter = 0


def get_prefix(client, message):
    with open("Arrays/prefixes.json", "r") as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]


client = commands.Bot(command_prefix=get_prefix, case_insensitive=True, intents=intents)
client.remove_command("help")

token = json.load(open("secrets.json", "r"))["secret"]

words = json.load(open("Arrays/forbidden_game_names.json", "r"))["game_names"]

websites = json.load(open("Arrays/links.json", "r"))["link"]

meter = json.load(open("Arrays/random_responses.json", "r"))["responses"][
    "random_response"
]

greetings = json.load(open("Arrays/random_responses.json", "r"))["responses"][
    "random_greetings"
]

activity = cycle(json.load(open("Arrays/status_options.json", "r"))["activity"])

status = cycle(json.load(open("Arrays/status_options.json", "r"))["status"])

offend = json.load(open("Arrays/Insult.json", "r"))["bad"]

config = json.load(open("config.json", "r"))

[
    DM_New_Member_Upon_Joining,
    Joining_Message,
    GIVE_ROLE_UPON_JOINING,
    role_ID,
    ALLOW_CUSTOM_MESSAGE,
    CUSTOM_MESSAGE_ON_MESSAGE,
    CUSTOM_MESSAGE_CHANCE,
] = [config[i] for i in config]

CUSTOM_MESSAGE_CHANCE = int(CUSTOM_MESSAGE_CHANCE)

randMessage = 1

randReaction = 1

LEVEL_SYSTEM = 1

# colors = [0xFFE4E1, 0x00FF7F, 0xD8BFD8, 0xDC143C, 0xFF4500, 0xDEB887, 0xADFF2F, 0x800000, 0x4682B4, 0x006400, 0x808080, 0xA0522D, 0xF08080, 0xC71585, 0xFFB6C1, 0x00CED1]


@client.event
async def on_ready():
    print("Bot is online!")
    change_status.start()


@client.event
async def on_guild_join(guild):
    with open("Arrays/prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = "!"

    with open("Arrays/prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)

    general = find(lambda x: x.name == "general", guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        await general.send(
            "https://i.pinimg.com/564x/37/ab/89/37ab89389766b74058bc5b38c2edc4b6.jpg"
        )
        await general.send(
            "DAFAQ? \nUse !help to learn more. \nUse !change_prefix to do the you know what ;)"
        )


@client.event
async def on_guild_remove(guild):
    with open("Arrays/prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open("Arrays/prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)


@client.event
async def on_member_join(member):

    # Auto adding roles upon joining
    # if GIVE_ROLE_UPON_JOINING == True:
    #     role = discord.utils.get(member.server.roles, id=f"<{role_ID}>")
    #     await member.add_roles(member, role)

    # # Dm new member upon joining
    # if DM_New_Member_Upon_Joining == True:
    #     channel = await member.create_dm()
    #     await channel.send(Joining_Message)

    # MESSAGE = False
    # if MESSAGE == True:
    #     channel = discord.utils.get(member.guild.text_channels, name="updates")
    #     await channel.send(f"{member} has joined the server")
    pass


@client.event
async def on_member_remove(member):
    # channel = discord.utils.get(member.guild.text_channels, name="updates")
    # await channel.send(f"{member} has left the server")
    pass


def Find(string):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, string)
    return [x[0] for x in url]


@client.event
async def on_message_delete(message):
    if message.guild.id != 691848461217169438 or message.guild.id != 756226688442171475:
        return
    channel = client.get_channel(843309207825678377)
    embed = discord.Embed(colour=random.randint(0, 0xFFFFFF))
    embed.set_footer(text=f"I am watching ;)")
    links = Find(message.content)

    if links:
        i = 0
        for y in links:
            words = message.content.replace(y, "[image]")
        for x in links:
            if i == 0:
                embed.add_field(
                    name=f"{message.author} deleted in ***{message.channel}*** from ***{message.guild.name}***:",
                    value=words,
                    inline=True,
                )
            else:
                embed.add_field(
                    name=f"{message.author} deleted in ***{message.channel}*** from ***{message.guild.name}***:",
                    value="** **",
                    inline=True,
                )
            embed.set_image(url=x)
            await channel.send(embed=embed)
            i += 1
        return

    embed.add_field(
        name=f"{message.author} deleted in ***{message.channel}*** from ***{message.guild.name}***:",
        value=message.content,
        inline=True,
    )
    await channel.send(embed=embed)


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
        global slientMember
        global sliencedMember
        global counter

        # if message.author.id == 578715287491182595:
        #     await message.channel.send(f"{slientMember}\n{sliencedMember}")

        if ALLOW_CUSTOM_MESSAGE == "True":
            print("true")
            if random.random() < CUSTOM_MESSAGE_CHANCE:
                print("method worked")
                current = random.randint(0, len(meter) - 1)
                while last == current:
                    current = random.randint(0, len(meter) - 1)
                last = current
                await message.channel.send(
                    f"<@{message.author.id}> {CUSTOM_MESSAGE_ON_MESSAGE[current]}"
                )
                return

        if randMessage == 1:
            random_num = random.random()
            if random_num < 0.0001:
                current = random.randint(0, len(meter) - 1)
                # global last
                while last == current:
                    current = random.randint(0, len(meter) - 1)
                last = current
                await message.channel.send(f"<@{message.author.id}> {meter[current]}")
                return
            elif random_num >= 0.0001 and random_num < 0.0002:
                current_web = random.randint(0, len(websites) - 1)
                # global last_web
                while last_web == current_web:
                    current_web = random.randint(0, len(websites) - 1)
                    last_web = current_web
                await message.channel.send(
                    f"<@{message.author.id}> NO TIME TO EXPLAIN, WE GOTTA GO!\n{websites[current_web]}"
                )
                return

        if randReaction == 1:
            if random.random() < 0.01:
                emoji = discord.utils.get(message.guild.emojis, name="pepePanties")
                if emoji:
                    await message.add_reaction(emoji)
                    return

        if message.content.startswith("hello"):
            if random.random() < 0.25:
                await message.channel.send(
                    f"<@{message.author.id}> {random.choice(greetings)}"
                )
                return

        for i in words:
            if i in message.content.lower():
                if random.random() < 0.01:
                    await message.channel.send(f"<@{message.author.id}> stfu")
                    return

        if (
            "calm leo" in message.content.lower()
            and "prefix" in message.content.lower()
        ):
            try:
                with open("Arrays/prefixes.json", "r") as f:
                    prefixes = json.load(f)

                await message.channel.send(prefixes[str(message.guild.id)])
            except:
                with open("Arrays/prefixes.json", "r") as f:
                    prefixes = json.load(f)

                prefixes[str(message.guild.id)] = "!"

                with open("Arrays/prefixes.json", "w") as f:
                    json.dump(prefixes, f, indent=4)

                with open("Arrays/prefixes.json", "r") as f:
                    await message.channel.send(prefixes[str(message.guild.id)])

        if slientMember and message.author.id == sliencedMember:
            if counter >= 5:
                slientMember = False
                counter = 0
                await message.channel.send(f"<@{sliencedMember}> You are now spared.")
                return
            await message.channel.purge(limit=1)
            await message.channel.send(
                f"<@{sliencedMember}> tried to open his filthy mouth."
            )
            counter += 1

    await client.process_commands(message)


@client.command(pass_context=True)
async def die(ctx):
    messages = await ctx.send(f"<@756208954031341688> is leaving the server.")
    await asyncio.sleep(1)
    await messages.edit(content=f"<@756208954031341688> is leaving the server..")
    await asyncio.sleep(1)
    await messages.edit(content=f"<@756208954031341688> is leaving the server...")
    await asyncio.sleep(1)
    await messages.edit(content=f"<@756208954031341688> is leaving the server.")
    await asyncio.sleep(1)
    await messages.edit(content=f"<@756208954031341688> is leaving the server..")
    await asyncio.sleep(1)
    await messages.edit(content=f"<@756208954031341688> is leaving the server...")
    await asyncio.sleep(1)
    await messages.edit(content=f"<@756208954031341688> has left the server!")
    await asyncio.sleep(2)
    await messages.edit(
        content=f"<@756208954031341688> LMAOOOO Got you!!\n(╯°□°）╯︵ ┻━┻\n┬─┬ ノ( ゜-゜ノ)"
    )
    StopAsyncIteration


@client.command()
async def howold(ctx, member: discord.Member):
    now = datetime.utcnow()
    delta = now - member.created_at
    year = int(delta.days / 365)
    day = delta.days % 365
    hour = delta.seconds // 3600
    minute = (delta.seconds // 60) % 60
    second = (delta.seconds // 3600) % 60
    await ctx.send(
        f"<@{member.id}>'s account is about {year} years {day} days {hour} hours {minute} minutes {second} seconds old!"
    )


@client.command()
async def emoji(ctx):
    embed = discord.Embed(colour=discord.Colour.orange())
    embed.set_author(
        name="Calm Leo",
        icon_url="https://i.pinimg.com/originals/8f/90/39/8f90394879fd28a09e09bf4faf7ee017.jpg",
    )
    # embed.set_thumbnail(url="https://i.pinimg.com/originals/8f/90/39/8f90394879fd28a09e09bf4faf7ee017.jpg")
    # embed.set_image(url="https://i.pinimg.com/originals/8f/90/39/8f90394879fd28a09e09bf4faf7ee017.jpg")
    embed.add_field(
        name="!panties", value="<:pepePanties:699414631923318845>", inline=True
    )
    embed.add_field(name="!laugh", value="<:kekw:717161197119471706>", inline=True)
    embed.add_field(name="!cry", value="<:monkaCry:717160567084679199>", inline=True)
    embed.add_field(
        name="!christ", value="<:monkaChrist:699414631453687888>", inline=True
    )
    embed.add_field(name="!think", value="<:monkaHmm:699414631801684020>", inline=True)
    embed.add_field(name="!scared", value="<:spooked:798027263349620787>", inline=True)
    embed.add_field(
        name="!glasses", value="<:anime_glasses:847307163939897344>", inline=True
    )
    embed.add_field(
        name="!drama", value="<:pepe_drama:847308076369707019>", inline=True
    )
    embed.add_field(name="!simp", value="<:simp:847307558367920211>", inline=True)
    embed.add_field(name="!thinker", value="<:thinker:847333996412928000>", inline=True)
    embed.add_field(name="!smile", value="<:smile:847336513906016287>", inline=True)
    embed.add_field(name="!wut", value="<:shaking_eye:847338523337293844>", inline=True)
    embed.add_field(name="!shock", value="<:shock:847880395579719716>", inline=True)
    embed.add_field(name="!woke", value="<:woke:847881227793072148>", inline=True)
    embed.add_field(
        name="!interested", value="<:interested:847881182430625872>", inline=True
    )
    await ctx.send(embed=embed)


@client.command()
async def interested(ctx):
    try:
        await ctx.message.channel.purge(limit=1)
    except:
        pass
    await ctx.message.channel.send("<:interested:847881182430625872>")


@client.command()
async def woke(ctx):
    try:
        await ctx.message.channel.purge(limit=1)
    except:
        pass
    await ctx.message.channel.send("<:woke:847881227793072148>")


@client.command()
async def shock(ctx):
    try:
        await ctx.message.channel.purge(limit=1)
    except:
        pass
    await ctx.message.channel.send("<:shock:847880395579719716>")


@client.command()
async def wut(ctx):
    try:
        await ctx.message.channel.purge(limit=1)
    except:
        pass
    await ctx.message.channel.send("<:shaking_eye:847338523337293844>")


@client.command()
async def smile(ctx):
    try:
        await ctx.message.channel.purge(limit=1)
    except:
        pass
    await ctx.message.channel.send("<:smile:847336513906016287>")


@client.command()
async def thinker(ctx):
    try:
        await ctx.message.channel.purge(limit=1)
    except:
        pass
    await ctx.message.channel.send("<:thinker:847333996412928000>")


@client.command()
async def simp(ctx):
    try:
        await ctx.message.channel.purge(limit=1)
    except:
        pass
    await ctx.message.channel.send("<:simp:847307558367920211>")


@client.command()
async def drama(ctx):
    try:
        await ctx.message.channel.purge(limit=1)
    except:
        pass
    await ctx.message.channel.send("<:pepe_drama:847308076369707019>")


@client.command()
async def glasses(ctx):
    try:
        await ctx.message.channel.purge(limit=1)
    except:
        pass
    await ctx.message.channel.send("<:anime_glasses:847307163939897344>")


@client.command()
async def panties(ctx):
    try:
        await ctx.message.channel.purge(limit=1)
    except:
        pass
    await ctx.message.channel.send("<:pepePanties:699414631923318845>")


@client.command()
async def laugh(ctx):
    try:
        await ctx.message.channel.purge(limit=1)
    except:
        pass
    await ctx.message.channel.send("<:kekw:717161197119471706>")


@client.command()
async def cry(ctx):
    try:
        await ctx.message.channel.purge(limit=1)
    except:
        pass
    await ctx.message.channel.send("<:monkaCry:717160567084679199>")


@client.command()
async def christ(ctx):
    try:
        await ctx.message.channel.purge(limit=1)
    except:
        pass
    await ctx.message.channel.send("<:monkaChrist:699414631453687888>")


@client.command()
async def think(ctx):
    try:
        await ctx.message.channel.purge(limit=1)
    except:
        pass
    await ctx.message.channel.send("<:monkaHmm:699414631801684020>")


@client.command()
async def scared(ctx):
    try:
        await ctx.message.channel.purge(limit=1)
    except:
        pass
    await ctx.message.channel.send("<:spooked:798027263349620787>")


@client.command()
async def getprefix(ctx):
    with open("Arrays/prefixes.json", "r") as f:
        prefixes = json.load(f)

    await ctx.send(prefixes[str(ctx.guild.id)])


@client.command()
async def change_prefix(ctx, prefix):
    if ctx.message.author.guild_permissions.administrator:
        prefixes = json.load(open("Arrays/prefixes.json", "r"))
        # default prefix
        prefixes[str(ctx.guild.id)] = prefix

        with open("Arrays/prefixes.json", "w") as f:
            json.dump(prefixes, f, indent=4)

        await ctx.send(f"The new prefix is now {prefix}")


@client.command()
async def ping(ctx):
    response = [
        f"Shut the fuck up {round(client.latency * 1000)}ms boy",
        f"Here you go kind sir: {round(client.latency*1000)}ms",
        "No",
    ]
    await ctx.send(random.choice(response))


@client.command(aliases=["8ball"])
async def _8ball(ctx, *, question):
    answer = ["Idk", "www.google.com", "https://imgur.com/gallery/TCmi3", "Yes!"]
    await ctx.send(f"Question: {question}\nAnswer: {random.choice(answer)}")


@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount + 1)


@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(
            f"<@{ctx.message.author.id}> You do not have the permission to edit messages."
        )


@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    if member.id == 578715287491182595:
        await ctx.send(
            f"<@{ctx.message.author.id}> HOW DARE YOU INSULT MY MASTER!!!\n{member.mention} My lord, what should I do with this big bruh?"
        )
        return
    if member.id == 756208954031341688:
        await ctx.send(
            f"<@{ctx.message.author.id}> You do not have the permission to kick **ME**."
        )
        return
    await member.kick(reason=reason)
    await ctx.send(f"Kicked {member.mention}\nreason: {reason}")


@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(
            f"<@{ctx.message.author.id}> You do not have the permission to kick members."
        )


@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    if member.id == 578715287491182595:
        await ctx.send(
            f"<@{ctx.message.author.id}> HOW DARE YOU INSULT MY MASTER!!!\n{member.mention} My lord, what should I do with this big bruh?"
        )
        return
    if member.id == 756208954031341688:
        await ctx.send(
            f"<@{ctx.message.author.id}> You do not have the permission to ban **ME**."
        )
        return
    await member.ban(reason=reason)
    await ctx.send(f"Banned {member.mention}\nreason: {reason}")


@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(
            f"<@{ctx.message.author.id}> You do not have the permission to ban members."
        )


@client.command()
@commands.has_permissions(kick_members=True)
async def silent(ctx, member: discord.Member):
    if counter != 0:
        await ctx.send(
            f"<@{ctx.message.author.id}> You can only persecute one person at a time."
        )
        return
    if member.id == 578715287491182595:
        await ctx.send(
            f"<@{ctx.message.author.id}> HOW DARE YOU INSULT MY MASTER!!!\n{member.mention} My lord, what should I do with this big bruh?"
        )
        return
    if member.id == 756208954031341688:
        await ctx.send(
            f"<@{ctx.message.author.id}> You do not have the permission to silence **ME**."
        )
        return

    global slientMember
    global sliencedMember

    slientMember = True
    sliencedMember = member.id

    # with open("Arrays/list.json", "r") as f:
    #     print("1")
    #     lists = json.load(f)
    #     print("2.5")
    # print("2")
    # lists[member.id] = "0"

    # with open("Arrays/list.json" , "w") as f:
    #     json.dump(lists, f, indent=4)

    await ctx.send(f"{member.mention} is now slienced.")


@client.command()
async def video(ctx):

    url = "https://youtube.com/playlist?list=PLAr0uSVISvMV9UejvuqnIumjOp5cV83LZ"
    query = parse_qs(urlparse(url).query, keep_blank_values=True)
    playlist_id = query["list"][0]

    youtube = googleapiclient.discovery.build(
        "youtube", "v3", developerKey=""
    )

    request = youtube.playlistItems().list(
        part="snippet", playlistId=playlist_id, maxResults=50
    )
    response = request.execute()

    playlist_items = []
    while request is not None:
        response = request.execute()
        playlist_items += response["items"]
        request = youtube.playlistItems().list_next(request, response)

    # print(f"total: {len(playlist_items)}")
    # print(
    #     [
    #         f'https://www.youtube.com/watch?v={t["snippet"]["resourceId"]["videoId"]}&list={playlist_id}&t=0s'
    #         for t in playlist_items
    #     ]
    # )
    index = random.randint(0, len(playlist_items) - 1)
    t = playlist_items[index]
    await ctx.send(
        f'https://www.youtube.com/watch?v={t["snippet"]["resourceId"]["videoId"]}&list={playlist_id}&t=0s'
    )

    # current_web = random.randint(0, len(websites) - 1)
    # global last_web
    # while last_web == current_web:
    #     current_web = random.randint(0, len(websites) - 1)
    #     last_web = current_web
    # await ctx.send(f"{websites[current_web]}")


@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"Unbanned {user.mention}")
            return


@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(
            f"<@{ctx.message.author.id}> You do not have the permission to unban members."
        )


@client.command()
async def tell(ctx, member: discord.Member, *, reason):
    if "/tts" in reason:
        nreason = reason.replace("/tts", "")
        await ctx.channel.purge(limit=1)
        await ctx.send(f"{member.mention} {nreason}", tts=True)
        return

    await ctx.channel.purge(limit=1)
    await ctx.send(f"{member.mention} {reason}")


@tell.error
async def tell_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument) or isinstance(
        error, commands.BadArgument
    ):
        await ctx.send(
            f"<@{ctx.message.author.id}> Bruh, you are using this command wrong...\nExample:\nInput: !tell <@{ctx.message.author.id}> You did something wrong!\nOutput: <@{ctx.message.author.id}> You did something wrong!"
        )


@client.command()
async def say(ctx, *, reason):
    if "/tts" in reason:
        nreason = reason.replace("/tts", "")
        await ctx.channel.purge(limit=1)
        await ctx.send(f"{nreason}", tts=True)
        return

    await ctx.channel.purge(limit=1)
    await ctx.send(f"{reason}")


@client.command()
async def unzip(ctx):
    await ctx.channel.purge(limit=1)
    await ctx.send(
        "https://i.chzbgr.com/full/8091158016/h223D6252/sigh-here-we-go-again"
    )


@client.command()
async def perhaps(ctx):
    await ctx.channel.purge(limit=1)
    await ctx.send("https://i.kym-cdn.com/photos/images/original/001/398/111/d5a")


@tell.error
async def say_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument) or isinstance(
        error, commands.BadArgument
    ):
        await ctx.send(
            f"<@{ctx.message.author.id}> Bruh, you are using this command wrong...\nExample:\nInput: !say You did something wrong!\nOutput: You did something wrong!"
        )


@client.command()
async def insult(ctx, member: discord.Member):
    if member.id == 578715287491182595:
        if random.random() < 0.5:
            await ctx.send(
                f"<@{ctx.message.author.id}> HOW DARE YOU INSULT MY MASTER!!!\n{member.mention} My lord, what should I do with this big bruh?"
            )
            return
    await ctx.send(f"{member.mention} {random.choice(offend)}")


@insult.error
async def insult_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument) or isinstance(
        error, commands.BadArgument
    ):
        await ctx.send(
            f"<@{ctx.message.author.id}> You can't even insult people correctly?\nHere is how:\n !insult <@{ctx.message.author.id}> {random.choice(offend)}"
        )


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(
            f"<@{ctx.message.author.id}> That is not a valid command for me!\nUse !help to check out all existing commands!\nB r u h"
        )


@client.command(pass_context=True)
async def meme(ctx):
    headers = {"User-Agent": "Calm Leo Bot Version 1.0"}
    num = random.random()
    if num <= 0.3:
        memes = json.load(open("Arrays/memes.json", "r"))["memes"]
        await ctx.send(random.choice(memes))
    elif num > 0.3 and num <= 0.6:
        i = 0
        error = 1
        while error != 0:
            # print(f"https://www.reddit.com/r/{names}/random.json")
            try:
                reddit_post = get(
                    f"https://www.reddit.com/r/memes/random.json", headers=headers
                ).json()
                await ctx.send(reddit_post[0]["data"]["children"][0]["data"]["url"])
                error = 0
            except:
                error = 1
                if i >= 5:
                    # print("end")
                    await ctx.send(
                        f"Hmmmm. Something went wrong)\n-brought to you by this command has failed **{i}** times gang"
                    )
                    return
                i = i + 1
                # print(f"Wrong\n {i}")
        # print("sent")
    else:
        i = 0
        error = 1
        # print(f"https://www.reddit.com/r/{names}/random.json")
        while error != 0:
            try:
                reddit_post = get(
                    f"https://www.reddit.com/r/dankmemes/random.json", headers=headers
                ).json()
                await ctx.send(reddit_post[0]["data"]["children"][0]["data"]["url"])
                error = 0
            except:
                error = 1
                if i >= 5:
                    # print("end")
                    await ctx.send(
                        f"Hmmmm. Something went wrong)\n-brought to you by this command has failed **{i}** times gang"
                    )
                    return
                i = i + 1
                # print(f"Wrong\n {i}")
            # print("sent")


@client.command(pass_context=True)
async def quote(ctx):
    quotes = json.load(open("Arrays/quotes.json", "r"))["quote"]
    embed = discord.Embed(colour=random.randint(0, 0xFFFFFF))
    embed.add_field(name="Quote", value=f"\n{random.choice(quotes)}", inline=False)
    await ctx.send(embed=embed)


@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(
        status=discord.Status.idle, activity=discord.Game(next(activity))
    )


def obtain_id(ctx):
    return ctx.author.id


def is_it_me(ctx):
    return obtain_id == 578715287491182595


@client.command(pass_context=True)
async def dm(ctx, member: discord.Member, *, content):
    channel = await member.create_dm()
    await channel.send(f"**{ctx.message.author} said:** {content}")
    await ctx.channel.purge(limit=1)


@client.command(pass_context=True)
async def pm(ctx, member: discord.Member, *, content):
    channel1 = await member.create_dm()
    await channel1.send(f"{content}")
    await ctx.channel.purge(limit=1)


@client.command
async def randMessage_on(ctx):
    if ctx.message.author.guild_permissions.administrator:
        if randMessage == 1:
            await ctx.send(
                f"<@{ctx.message.author.id}> Random_Message is already on..."
            )
            return
        randMessage = 1
        await ctx.send(f"<@{ctx.message.author.id}> Random_Message is now on!")
    else:
        await ctx.send(
            f"<@{ctx.message.author.id}> You don't have the permission to enable Random_Message."
        )


# @randMessage_on.error
# async def enable_randMessage_error(ctx):
#     pass


@client.command
async def randMessage_off(ctx):
    if ctx.message.author.guild_permissions.administrator:
        if randMessage == 0:
            await ctx.send(
                f"<@{ctx.message.author.id}> Random_Message is already off..."
            )
            return
        randMessage = 0
        await ctx.send(f"<@{ctx.message.author.id}> Random_Message is now off!")
    else:
        await ctx.send(
            f"<@{ctx.message.author.id}> You don't have the permission to disable Random_Message."
        )


# @randMessage_off.error
# async def disable_randMessage_error(ctx):
#     pass


@client.command
async def randReact_on(ctx):
    if ctx.message.author.guild_permissions.administrator:
        if randReaction == 1:
            await ctx.send(
                f"<@{ctx.message.author.id}> Random_Reaction is already on..."
            )
            return
        randReaction = 1
        await ctx.send(f"<@{ctx.message.author.id}> Random_Reaction is now on!")
    else:
        await ctx.send(
            f"<@{ctx.message.author.id}> You don't have the permission to enable Random_Reaction."
        )


@client.command
async def randReact_off(ctx):
    if ctx.message.author.guild_permissions.administrator:
        if randReaction == 0:
            await ctx.send(
                f"<@{ctx.message.author.id}> Random_Message is already off..."
            )
            return
        randReaction = 0
        await ctx.send(f"<@{ctx.message.author.id}> Random_Message is now off!")
    else:
        await ctx.send(
            f"<@{ctx.message.author.id}> You don't have the permission to disable Random_Reaction."
        )


@client.command()
async def waifu(ctx):
    headers = {"User-Agent": "Calm Leo Bot Version 1.0"}
    i = 0
    error = 1
    Random = random.random()
    while error != 0:
        try:
            reddit_post = get(
                "https://www.reddit.com/r/animegirls/random.json", headers=headers
            ).json()

            await ctx.send(reddit_post[0]["data"]["children"][0]["data"]["url"])
            error = 0
        except:
            error = 1
            if i >= 5:
                # print("end")
                await ctx.send(
                    f"Hmmmm. Something went wrong)\n-brought to you by this command has failed **{i}** times gang"
                )
                return
            i = i + 1
            # print("Wrong")


@client.command()
async def jojo(ctx):
    headers = {"User-Agent": "Calm Leo Bot Version 1.0"}
    i = 0
    error = 1
    while error != 0:
        try:
            reddit_post = get(
                "https://www.reddit.com/r/ShitPostCrusaders/random.json",
                headers=headers,
            ).json()
            await ctx.send(reddit_post[0]["data"]["children"][0]["data"]["url"])
            error = 0
        except:
            error = 1
            if i >= 5:
                # print("end")
                await ctx.send(
                    f"Hmmmm. Something went wrong)\n-brought to you by this command has failed **{i}** times gang"
                )
                return
            i = i + 1
            # print("Wrong")


@client.command()
async def amongus(ctx):
    headers = {"User-Agent": "Calm Leo Bot Version 1.0"}
    i = 0
    error = 1
    while error != 0:
        try:
            reddit_post = get(
                "https://www.reddit.com/r/amogus/random.json", headers=headers
            ).json()
            await ctx.send(reddit_post[0]["data"]["children"][0]["data"]["url"])
            error = 0
        except:
            error = 1
            if i >= 5:
                # print("end")
                await ctx.send(
                    f"Hmmmm. Something went wrong)\n-brought to you by this command has failed **{i}** times gang"
                )
                return
            i = i + 1
            # print("Wrong")


@client.command()
async def reddit(ctx, *, name=None):
    if name == None:
        embed = discord.Embed(colour=discord.Colour.orange())
        embed.set_author(
            name="Calm Leo",
            icon_url="https://i.pinimg.com/originals/8f/90/39/8f90394879fd28a09e09bf4faf7ee017.jpg",
        )
        embed.add_field(
            name="!reddit [*subreddit name*]",
            value="Image from that subreddit",
            inline=True,
        )
        embed.add_field(name="!waifu", value="WAIFU", inline=True)
        embed.add_field(name="!jojo", value="Jojo memes", inline=True)
        embed.add_field(name="!meme", value="Displays a meme", inline=True)
        embed.add_field(name="!amongus", value="AMOGUS", inline=True)
        embed.add_field(name="!youtube", value="Random YouTube videos", inline=True)
        embed.add_field(name="!hentai", value="random doujins", inline=True)
        await ctx.send(embed=embed)
        return

    headers = {"User-Agent": "Calm Leo Bot Version 1.0"}
    names = name.replace(" ", "")
    i = 0
    error = 1
    # print(f"https://www.reddit.com/r/{names}/random.json")
    while error != 0:
        try:
            reddit_post = get(
                f"https://www.reddit.com/r/{names}/random.json", headers=headers
            ).json()
            if reddit_post[0]["data"]["children"][0]["data"]["over_18"] == 1:
                if ctx.channel.is_nsfw() != 1:
                    await ctx.send("No NSFW post in non-NSFW channels!!! ¯\_(ツ)_/¯")
                    return
                # if(random.random() <= 0.75):
                #     await ctx.send("HMMMM. Is this NSFW? (╯°□°）╯︵ ┻━┻")
                #     return
                await ctx.send("NSFW post? ( ͡☉⁄ ⁄ ͜⁄ ͜ʖ̫⁄ ⁄ ͡☉)")
            await ctx.send(reddit_post[0]["data"]["children"][0]["data"]["url"])
            error = 0
        except:
            error = 1
            if i >= 5:
                # print("end")
                await ctx.send(
                    f"Either this subreddit doesn't exist or I am too dumb.\nIt's probably the latter ;)\n-brought to you by this command has failed **{i}** times gang"
                )
                return
            i = i + 1
            # print(f"Wrong\n {i}")
    # print("sent")


@client.command()
async def youtube(ctx):
    headers = {"User-Agent": "Calm Leo Bot Version 1.0"}
    i = 0
    error = 1
    # print(f"https://www.reddit.com/r/{names}/random.json")
    while error != 0:
        try:
            reddit_post = get(
                f"https://www.reddit.com/r/deepintoyoutube/random.json", headers=headers
            ).json()
            await ctx.send(reddit_post[0]["data"]["children"][0]["data"]["url"])
            error = 0
        except:
            error = 1
            if i >= 5:
                # print("end")
                await ctx.send(
                    f"Either this subreddit doesn't exist or I am too dumb.\nIt's probably the latter ;)\n-brought to you by this command has failed **{i}** times gang"
                )
                return
            i = i + 1
            # print(f"Wrong\n {i}")
    # print("sent")


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
            if d.upvotes > temp:
                j = i
                temp = d.upvotes

        i = 0
        for d in defs:
            if i == j:
                embed = discord.Embed(colour=discord.Colour.green())
                embed.set_footer(text=f"{d.upvotes} upvotes")
                # embed.set_author(name=f"{term}")
                embed.add_field(
                    name=f"{term.upper()}", value=f"{d.definition}", inline=True
                )
                await ctx.send(embed=embed)
                return
            i = i + 1

        # error handling
        embed = discord.Embed(colour=discord.Colour.green())
        embed.set_footer(
            text=f"Something went wrong and I am extremely sorry\n┬─┬ ノ( ゜-゜ノ)"
        )
        embed.add_field(
            name=f"I DON'T FUCKING KNOW!",
            value=f"Go google it yourself you lazy piece of bruh\n(╯°□°）╯︵ ┻━┻",
            inline=True,
        )
        await ctx.send(embed=embed)

    except:
        embed = discord.Embed(colour=discord.Colour.green())
        embed.set_footer(
            text=f"Something went wrong and I am extremely sorry\n┬─┬ ノ( ゜-゜ノ)"
        )
        embed.add_field(
            name=f"I DON'T FUCKING KNOW!",
            value=f"Go google it yourself you lazy piece of bruh\n(╯°□°）╯︵ ┻━┻",
            inline=True,
        )
        await ctx.send(embed=embed)


@client.command()
async def profilepic(ctx, member: Member = None):
    if not member:
        member = ctx.author
    await ctx.send(member.avatar_url)


@client.command()
async def beans(ctx):
    await ctx.send("https://ifunny.co/video/GPNeYfUL8")


@client.command()
async def hentai(ctx):
    if ctx.channel.is_nsfw() != 1:
        await ctx.send("No NSFW post in non-NSFW channels!!! ¯\_(ツ)_/¯")
        return
    try:
        nhentai = NHentai()
        Doujin = nhentai.get_random()
        page = random.randrange(0, Doujin.total_pages)
        await ctx.send(Doujin.images[page])
    except:
        await ctx.send("Toooo spicyyyy!!! ¬‿¬")


@client.command()
async def search(ctx, *, term):
    if ctx.channel.is_nsfw() != 1:
        await ctx.send("No NSFW post in non-NSFW channels!!! ¯\_(ツ)_/¯")
        return
    try:
        nhentai = NHentai()
        SearchPage = nhentai.search(query=term, sort="popular", page=1)
        # await ctx.send(SearchPage.doujins[0].id)
        Doujin = nhentai._get_doujin(id=SearchPage.doujins[0].id)
        page = random.randrange(0, Doujin.total_pages)
        await ctx.send(Doujin.images[page])
    except:
        await ctx.send("Toooo spicyyyy!!! ¬‿¬")


@client.command()
async def poll(ctx, *, question):
    yesvote = 0
    novote = 0

    await ctx.channel.purge(limit=1)
    embed = discord.Embed(color=discord.Color.dark_blue())
    embed1 = discord.Embed(color=discord.Color.dark_blue())
    embed.set_author(name=f"{question}")
    embed1.set_author(name=f"{question}")

    embed.add_field(name="OPTIONS", value="**✅ = Yes**\n**❌ = No**")
    message = await ctx.send(embed=embed)
    await message.add_reaction("✅")
    await message.add_reaction("❌")

    # reaction, user = await client.wait_for("reaction_add")
    # if(reaction == ":white_check_mark:"):
    #     yesvote += 1
    # elif(reaction == ":x:"):
    #     novote += 1
    # await ctx.send(reaction);
    # embed1.add_field(name= "OPTIONS",value=f"**✅ = {yesvote} votes**\n**❌ = {novote} votes**", inline=False)
    # await message.edit(embed=embed1)


@client.command()
async def help(ctx, page=1):
    embed = discord.Embed(colour=discord.Colour.orange())
    embed.set_author(
        name="Calm Leo",
        icon_url="https://i.pinimg.com/originals/8f/90/39/8f90394879fd28a09e09bf4faf7ee017.jpg",
    )
    # embed.set_thumbnail(url="https://i.pinimg.com/originals/8f/90/39/8f90394879fd28a09e09bf4faf7ee017.jpg")
    # embed.set_image(url="https://i.pinimg.com/originals/8f/90/39/8f90394879fd28a09e09bf4faf7ee017.jpg")
    if page == 1:
        embed.add_field(
            name="!change_prefix [*prefix*]", value="Change the prefix", inline=True
        )
        embed.add_field(
            name="!reddit [*subreddit name*]",
            value="Image from that subreddit",
            inline=True,
        )
        embed.add_field(
            name="!ud (*word*)",
            value="Looks up the word on urban dictionary",
            inline=True,
        )
        embed.add_field(name="!emoji", value="Sends custom emojis", inline=True)
        embed.add_field(
            name="!profilepic (*user*)", value="Get user's profile picture", inline=True
        )
        embed.add_field(
            name="!howold (*user*)", value="Get the age of the account", inline=True
        )
        embed.add_field(
            name="!insult (*user*)", value="Insults designated member", inline=True
        )
        embed.add_field(
            name="!say [*message*]",
            value="bot sends the designated message",
            inline=True,
        )
        embed.add_field(
            name="!tell (*user*) [*message*]",
            value="@ and sends the designated member the message",
            inline=True,
        )
        embed.add_field(
            name="!dm (*user*)[*message here]",
            value="Direct-messages a member of your choice(with name)",
            inline=True,
        )
        embed.add_field(
            name="!pm (*user*) [*message here*]",
            value="Private-messages a member of your choice(no name)",
            inline=True,
        )
        embed.add_field(name="!poll [*question*]", value="Start a poll", inline=True)
        embed.set_footer(text="!help 2 for troll commands")
        await ctx.send(embed=embed)
    elif page == 2:
        embed.add_field(name="!search", value="Searchs on nhentai", inline=True)
        embed.add_field(name="!waifu", value="WAIFU", inline=True)
        embed.add_field(name="!jojo", value="Jojo memes", inline=True)
        embed.add_field(name="!meme", value="Displays a meme", inline=True)
        embed.add_field(name="!amongus", value="AMOGUS", inline=True)
        embed.add_field(name="!video", value="Quality meme videos", inline=True)
        embed.add_field(name="!youtube", value="Random YouTube videos", inline=True)
        embed.add_field(name="!unzip", value="DON'T USE IT", inline=True)
        embed.add_field(name="!perhaps", value="DON'T USE THIS EITHER", inline=True)
        embed.add_field(name="!beans", value="BEANS", inline=True)
        embed.add_field(name="!hentai", value="random doujins", inline=True)
        embed.set_footer(text="!help 3 for help commands")
        await ctx.send(embed=embed)
    elif page == 3:
        embed.add_field(
            name="!help", value="Displays all available commands", inline=True
        )
        embed.add_field(
            name="!modhelp",
            value="Displays all available commands for moderators",
            inline=True,
        )
        embed.add_field(
            name="!devhelp",
            value="Displays all available commands for developers",
            inline=True,
        )
        embed.set_footer(text="Last Page")
        await ctx.send(embed=embed)


@client.command()
async def modhelp(ctx):
    embed = discord.Embed(colour=discord.Colour.red())
    embed.add_field(
        name="!clear", value="Clears a desginated number of messages", inline=True
    )
    embed.add_field(
        name="!kick *member*", value="Kicks a member(if with permission)", inline=True
    )
    embed.add_field(
        name="!ban *member*", value="Bans a member(if with permission)", inline=True
    )
    embed.add_field(
        name="!unban *member*", value="Unbans a member(if with permission)", inline=True
    )
    embed.add_field(name="!ping", value="Bot's ping(most of the times)", inline=True)
    embed.add_field(
        name="*what calm leo prefix*",
        value="displays the prefix (this is not a command)",
        inline=True,
    )
    await ctx.send(embed=embed)


@client.command()
async def devhelp(ctx):
    embed = discord.Embed(colour=discord.Colour.blue())
    embed.add_field(
        name="!change_prefix [*prefix*]", value="Change the prefix", inline=True
    )
    embed.add_field(
        name="!randMessage_on",
        value="allows the bot to send random messages",
        inline=True,
    )
    embed.add_field(
        name="!randMessage_off",
        value="prevents the bot to send random messages",
        inline=True,
    )
    embed.add_field(
        name="!randReact_on",
        value="allows the bot to randomly add a reaction to a message",
        inline=True,
    )
    embed.add_field(
        name="!randReact_off",
        value="prevents the bot from randomly adding a reaction to a message",
        inline=True,
    )
    embed.add_field(
        name="!8ball *question here*", value="Answers your question", inline=True
    )
    await ctx.send(embed=embed)


client.run(token)
