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
        meter = [f"<@{message.author.id}> That's kinda gay",
                f"<@{message.author.id}> There is always time for anime!",
                f"<@{message.author.id}> Sometimes, it takes a real man to be the best girl!"]
        if random.random() < 0.75:
            await message.channel.send(random.choice(meter))
            return
        else:
            websites = [f"https://www.crunchyroll.com/",
                    f"https://ifunny.co/",
                    "https://www.youtube.com/watch?v=Ta_WeP577Mg&list=LL6OKLcG9rx2rM07-fu_D93g&index=2&t=0s",
                    "https://www.youtube.com/watch?v=CQtIu-jZwHM&list=LL6OKLcG9rx2rM07-fu_D93g&index=6",
                    "https://www.youtube.com/watch?v=IgKUjVuRMR4&list=LL6OKLcG9rx2rM07-fu_D93g&index=9",
                    "https://www.youtube.com/watch?v=ShBtK1eYacY&list=LL6OKLcG9rx2rM07-fu_D93g&index=11",
                    "https://www.youtube.com/watch?v=eAVpNs37Lpk&list=LL6OKLcG9rx2rM07-fu_D93g&index=12",
                    "https://www.youtube.com/watch?v=tMhabr5odpw&list=LL6OKLcG9rx2rM07-fu_D93g&index=13",
                    "https://www.youtube.com/watch?v=yE5_eXP5ZmM&list=LL6OKLcG9rx2rM07-fu_D93g&index=14",
                    "https://www.youtube.com/watch?v=5bz1iDBFinM&list=LL6OKLcG9rx2rM07-fu_D93g&index=20",
                    "https://www.youtube.com/watch?v=caj7xEvjDiE&list=LL6OKLcG9rx2rM07-fu_D93g&index=23",
                    "https://www.youtube.com/watch?v=HPjJCVylFBo&list=LL6OKLcG9rx2rM07-fu_D93g&index=24",
                    "https://www.youtube.com/watch?v=S_5wDJKP3PI&list=LL6OKLcG9rx2rM07-fu_D93g&index=27",
                    "https://www.youtube.com/watch?v=QqeoDFaC1Tc&list=LL6OKLcG9rx2rM07-fu_D93g&index=30",
                    "https://www.youtube.com/watch?v=eM3BuVvXFy0&list=LL6OKLcG9rx2rM07-fu_D93g&index=34",
                    "https://www.youtube.com/watch?v=wAUK9hVgmNI&list=LL6OKLcG9rx2rM07-fu_D93g&index=40",
                    "https://www.youtube.com/watch?v=1iG_d0tgZEY&list=LL6OKLcG9rx2rM07-fu_D93g&index=47",
                    "https://www.youtube.com/watch?v=H8PXq3I0bsE&list=LL6OKLcG9rx2rM07-fu_D93g&index=49",
                    "https://www.youtube.com/watch?v=MDnP0RAtV7Q&list=LL6OKLcG9rx2rM07-fu_D93g&index=52",
                    "https://www.youtube.com/watch?v=zOAVZV8tLsc&list=LL6OKLcG9rx2rM07-fu_D93g&index=53",
                    "https://www.youtube.com/watch?v=0H6n1aK0ZSo&list=LL6OKLcG9rx2rM07-fu_D93g&index=57",
                    "https://www.youtube.com/watch?v=RkJzJgamF6o&list=LL6OKLcG9rx2rM07-fu_D93g&index=58",
                    "https://www.youtube.com/watch?v=cuERlyD0u2Q&list=LL6OKLcG9rx2rM07-fu_D93g&index=62",
                    "https://www.youtube.com/watch?v=zhf1pIl007o&list=LL6OKLcG9rx2rM07-fu_D93g&index=63",
                    "https://www.youtube.com/watch?v=QzWlxYNUTLI&list=LL6OKLcG9rx2rM07-fu_D93g&index=66",
                    "https://www.youtube.com/watch?v=0MW0mDZysxc&list=LL6OKLcG9rx2rM07-fu_D93g&index=67",
                    "https://www.youtube.com/watch?v=8UjWwMtrETk&list=LL6OKLcG9rx2rM07-fu_D93g&index=68",
                    "https://www.youtube.com/watch?v=QA-3du32tHM&list=LL6OKLcG9rx2rM07-fu_D93g&index=69",
                    "https://www.youtube.com/watch?v=CL_BTmrrZW8&list=LL6OKLcG9rx2rM07-fu_D93g&index=70",
                    "https://www.youtube.com/watch?v=yi8WrSCDfTY&list=LL6OKLcG9rx2rM07-fu_D93g&index=71",
                    "https://www.youtube.com/watch?v=I2p-PUQurxU&list=LL6OKLcG9rx2rM07-fu_D93g&index=73",
                    "https://www.youtube.com/watch?v=v-bOI2tggYE&list=LL6OKLcG9rx2rM07-fu_D93g&index=76",
                    "https://www.youtube.com/watch?v=9wykFW8W8HQ&list=LL6OKLcG9rx2rM07-fu_D93g&index=85",
                    "https://www.youtube.com/watch?v=XxBeM3ywcOw&list=LL6OKLcG9rx2rM07-fu_D93g&index=90",
                    "https://www.youtube.com/watch?v=Wb3UrJjAac4&list=LL6OKLcG9rx2rM07-fu_D93g&index=91",
                    "https://www.youtube.com/watch?v=zbQIp4-ZVD0&list=LL6OKLcG9rx2rM07-fu_D93g&index=92",
                    "https://www.youtube.com/watch?v=D9-voINFkCg&list=LL6OKLcG9rx2rM07-fu_D93g&index=94",
                    "https://www.youtube.com/watch?v=O3qhymqb7Jk&list=LL6OKLcG9rx2rM07-fu_D93g&index=95",
                    "https://www.youtube.com/watch?v=pC6ONIF7D3E&list=LL6OKLcG9rx2rM07-fu_D93g&index=117",
                    "https://www.youtube.com/watch?v=LldOqayU-rg&list=LL6OKLcG9rx2rM07-fu_D93g&index=121",
                    "https://www.youtube.com/watch?v=hQyhLZsw7e4&list=LL6OKLcG9rx2rM07-fu_D93g&index=133",
                    "https://www.youtube.com/watch?v=MHqr_SnZJJc&list=LL6OKLcG9rx2rM07-fu_D93g&index=138",
                    "https://www.youtube.com/watch?v=giS0BrfXUmM&list=LL6OKLcG9rx2rM07-fu_D93g&index=146",
                    "https://www.youtube.com/watch?v=kGl-tq7OVEE&list=LL6OKLcG9rx2rM07-fu_D93g&index=147",
                    "https://www.youtube.com/watch?v=_czzkqPjvS4&list=LL6OKLcG9rx2rM07-fu_D93g&index=159",
                    "https://www.youtube.com/watch?v=MmdmiFvOvsg&list=LL6OKLcG9rx2rM07-fu_D93g&index=166",
                    "https://www.youtube.com/watch?v=OXvAT7vZMuA&list=LL6OKLcG9rx2rM07-fu_D93g&index=165",
                    "https://www.youtube.com/watch?v=iAKB3Qj3PZU&list=LL6OKLcG9rx2rM07-fu_D93g&index=200",
                    "https://www.youtube.com/watch?v=hJsh3xoUHPc&list=LL6OKLcG9rx2rM07-fu_D93g&index=227",
                    "https://www.youtube.com/watch?v=MSIxlhIPxIQ&list=LL6OKLcG9rx2rM07-fu_D93g&index=230"]
            await message.channel.send(f"<@{message.author.id}> NO TIME TO EXPLAIN, WE GOTTA GO!\n{random.choice(websites)}")
            return
    

    if "gay" in message.content.lower():
        if random.random() < 0.2:
            await message.channel.send(f"<@{message.author.id}> Leo, is that you?")

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