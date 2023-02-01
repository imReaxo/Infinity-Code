#----IMPORT LIBS----#
import discord
import aiofiles
import yaml
import os
from discord.ext import commands
from pil import Image, ImageDraw, ImageFont, ImageChops
from io import BytesIO
#----IMPORT LIBS----#


#----IMPORT FROM CONFIG----#
with open("config.yml", "r") as file:
    config = yaml.safe_load(file)
#----IMPORT FROM CONFIG----#


#----CLIENT BASE----#
intents = discord.Intents().all()
client = commands.Bot(command_prefix=config['PREFIX'], intents=intents)
#----CLIENT BASE----#

#----CLIENT ON READY----#
@client.event
async def on_ready():
    for file in ["welcome_channels.txt", "goodbye_channels.txt"]:
        async with aiofiles.open(file, mode="a") as temp:
            pass
        
    async with aiofiles.open("welcome_channels.txt", mode="r") as file:
        lines = await file.readlines()
        for line in lines:
            data = line.split(" ")
            client.welcome_channels[int(data[0])] = (int(data[1]), " ".join(data[2:]).strip("\n"))
    async with aiofiles.open("goodbye_channels.txt", mode="r") as file:
        lines = await file.readlines()
        for line in lines:
            data = line.split(" ")
            client.goodbye_channels[int(data[0])] = (int(data[1]), " ".join(data[2:]).strip("\n"))
    print('♾ Infinty Code Team ♾')
#----CLIENT ON READY----#


#----WELCOMER & GOODBYER SETUP----#
client.welcome_channels = {}
client.goodbye_channels = {}


@client.command()
async def setup_welcomer(ctx, new_channel: discord.TextChannel=None, *, message=None):
    if new_channel != None and message != None:
        for channel in ctx.guild.channels:
            if channel == new_channel:
                client.welcome_channels[ctx.guild.id] = (channel.id, message)
                await ctx.channel.send(f"successfully ✅")
                async with aiofiles.open("welcome_channels.txt", mode="a") as file:
                    await file.write(f"{ctx.guild.id} {new_channel.id} {message}\n")
                return
        await ctx.channel.send("Couldn't find the given channel ❌")
    else:
        await ctx.channel.send("You didn't include the name of a welcome channel or a welcome message ❌")

@client.command()
async def setup_goodbyer(ctx, new_channel: discord.TextChannel=None, *, message=None):
    if new_channel != None and message != None:
        for channel in ctx.guild.channels:
            if channel == new_channel:
                client.goodbye_channels[ctx.guild.id] = (channel.id, message)
                await ctx.channel.send(f"successfully ✅")
                async with aiofiles.open("goodbye_channels.txt", mode="a") as file:
                    await file.write(f"{ctx.guild.id} {new_channel.id} {message}\n")
                return
        await ctx.channel.send("Couldn't find the given channel ❌")
    else:
        await ctx.channel.send("You didn't include the name of a goodbye channel or a goodbye message ❌")

#----WELCOMER & GOODBYER SETUP----#


#----WELCOMER & GOODBYER IMAGE MAKER----#
def circle(pfp,size = (215,215)):

    pfp = pfp.resize(size, Image.Resampling.LANCZOS).convert("RGBA")

    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask) 
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size, Image.Resampling.LANCZOS)
    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)
    return pfp
#----WELCOMER & GOODBYER IMAGE MAKER----#

#----WELCOMER & GOODBYER----#
@client.event
async def on_member_join(member):
    name = member.name
    tags = member.discriminator
    tag = f"#{tags}"
    base = Image.open("assets/Welcomer/welcome.png").convert("RGBA")
    pfp = member.display_avatar.replace(size=128)
    data = BytesIO(await pfp.read())
    pfp = Image.open(data).convert("RGBA")
    draw = ImageDraw.Draw(base)
    pfp = circle(pfp, (164,164))
    font = ImageFont.truetype("assets/fonts/main.ttf",38)
    draw.text((270,70),name,font = font)
    draw.text((531,120),tag,font = font)
    base.paste(pfp, (65,39), pfp)
    with BytesIO() as a:
        base.save(a,"PNG")
        a.seek(0)
        for guild_id in client.welcome_channels:
            if guild_id == member.guild.id:
                channel_id, message = client.welcome_channels[guild_id]
                await client.get_guild(guild_id).get_channel(channel_id).send(f"{member.mention} {message}👋", file = discord.File(a,"welcome.png"))
                return

@client.event
async def on_member_remove(member):
    name = member.name
    tags = member.discriminator
    tag = f"#{tags}"
    base = Image.open("assets/Goodbyer/goodbye.png").convert("RGBA")
    pfp = member.display_avatar.replace(size=128)
    data = BytesIO(await pfp.read())
    pfp = Image.open(data).convert("RGBA")
    draw = ImageDraw.Draw(base)
    pfp = circle(pfp, (164,164))
    font = ImageFont.truetype("assets/fonts/main.ttf",38)
    draw.text((270,70),name,font = font)
    draw.text((531,120),tag,font = font)
    base.paste(pfp, (65,39), pfp)
    with BytesIO() as a:
        base.save(a,"PNG")
        a.seek(0)
        for guild_id in client.goodbye_channels:
            if guild_id == member.guild.id:
                channel_id, message = client.goodbye_channels[guild_id]
                await client.get_guild(guild_id).get_channel(channel_id).send(f"{member.mention} {message}👋",file=discord.File(a, "goodbye.png"))
                return
#----WELCOMER & GOODBYER----#




client.run(config["TOKEN"])