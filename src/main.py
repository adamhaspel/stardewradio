import sys
import os
from dotenv import load_dotenv
from stringcolor import *
import time
import nextcord
from nextcord.ext import commands
import random
from mutagen import File
import asyncio
from pydub import AudioSegment
import shutil

TESTING_GUILD_ID = 1386354564441182268

if len(sys.argv) == 1:
    tokentype = input("> ")
else:
    tokentype = sys.argv[1]

while True:
    load_dotenv("env/.env")

    token = os.getenv(tokentype)
    if token == None:
        tokentype = input(cs(f"[{time.ctime()}] Startup Error: Not a set token", "red") + "\n> ")
        continue
    break
os.system('clear')

intents = nextcord.Intents.default()
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix="r!", intents=intents)
global song
global songtime

@bot.event
async def on_connect():
    print(cs(f'[{time.ctime()}] Info: Logging in as {bot.user.name}. Please stand by...', "green"))
    while True:
        if os.path.exists("env/out"):
            shutil.rmtree("env/out")
            print(cs(f'[{time.ctime()}] Info: Out folder cleared as per routine.', "green"))
        await asyncio.sleep(300)


@bot.event
async def on_ready():
    if not os.path.exists("env/out"):
        os.mkdir("env/out")
    print(cs(f'[{time.ctime()}] Info: {bot.user.name} is ready to function.', "green"))
    await asyncio.sleep(.5)
    print(cs(f'[{time.ctime()}] Info: Radio is online.', "green"))
    while True:
        global song
        global songtime
        song = random.choice(os.listdir("assets/audio/ost"))
        if song == "ConcernedApe - Stardew Valley OST - 100 Summit Celebration.mp3":
            songname = song[40:][:len(song) - 44]
        else:
            songname = song[39:][:len(song) - 43]
        audio = File(f"assets/audio/ost/{song}")
        if audio and hasattr(audio.info, 'length'):
            length = audio.info.length
        for i in bot.guilds:
            if bot.get_guild(i.id).voice_client:
                source = nextcord.FFmpegPCMAudio(f"assets/audio/ost/{song}")
                source = nextcord.PCMVolumeTransformer(source)
                source.volume = bot.get_guild(i.id).voice_client.volume
                while True:
                    try:
                        bot.get_guild(i.id).voice_client.play(source)
                    except:
                        continue
                    break
        xtra = ""
        if round(length % 60) < 10:
            xtra = "0"
        print(cs(f'[{time.ctime()}] Song: Now playing "{songname}" for 0{round(length/60)}:{xtra}{round(length % 60)}.', "green"))
        songtime = 0
        await bot.change_presence(activity=nextcord.Game(name=f"{songname}. Use r!help for more info."))
        while songtime <= length:
            await asyncio.sleep(1)
            songtime += 1

@bot.event
async def on_disconnect():
    for i in bot.guilds:
        if bot.get_guild(i.id).voice_client:
            await bot.get_guild(i.id).voice_client.disconnect()
    print(cs(f'[{time.ctime()}] Info: Disconnecting from {bot.user.name}. Please stand by...', "green"))

@bot.event
async def on_close():
    for i in bot.guilds:
        if bot.get_guild(i.id).voice_client:
            await bot.get_guild(i.id).voice_client.stop()
    await asyncio.sleep(1)
    print(cs(f'\r[{time.ctime()}] Info: {bot.user.name} is logging off.', "green"))

@bot.command(help="Connects the bot to a voice channel", aliases=["connect"])
async def join(ctx):
    global song
    global songtime
    if not ctx.author.voice:
        await ctx.send("```You are not in a voice channel. You must be in a voice channel to use this command.```")
        return
    else:
        if ctx.voice_client:
            if ctx.author.voice.channel == ctx.voice_client.channel:
                await ctx.send("```I have already joined your voice channel.```")
                return
            else:
                await ctx.send(f"```Moving to {ctx.author.voice.channel.name}...```")
                await ctx.voice_client.move_to(ctx.author.voice.channel)
        else:
            await ctx.send(f"```Joining {ctx.author.voice.channel.name}...```")
            await ctx.author.voice.channel.connect()
    ctx.voice_client.volume = 1
    input_file = f"assets/audio/ost/{song}"
    output_file = f"env/out/{ctx.guild.id}.mp3"
    start_time = round((9 + songtime)* 1000)
    audio = File(f"assets/audio/ost/{song}")
    end_time = round(1000* audio.info.length)
    audio = AudioSegment.from_mp3(input_file)
    sliced_audio = audio[start_time:end_time]
    sliced_audio.export(output_file, format="mp3")
    source = nextcord.FFmpegPCMAudio(f"assets/audio/sfx/syntheffect1.mp3")
    source.volume = ctx.voice_client.volume
    ctx.voice_client.play(source)
    while True:
        try:
            source = nextcord.FFmpegPCMAudio(f"env/out/{ctx.guild.id}.mp3")
            source.volume = ctx.voice_client.volume
            ctx.voice_client.play(source)
            break
        except:
            await asyncio.sleep(1)
            continue

@bot.command(help="Changes the volume of the radio")
async def volume(ctx, volume=None):
    global song
    global songtime
    if volume:
        if not ctx.voice_client:
            await ctx.send("```I am not in a voice channel. I must be in a voice channel to use this command.```")
            return
        else:
            if ctx.author.voice:
                if (not ctx.author.voice.channel == ctx.voice_client.channel) or not ctx.author.guild_permissions.move_members:
                    await ctx.send("```We are not in the same voice channel. We must be in the same voice channel to use this command.```")
                    return
                else:
                    pass
            else:
                if ctx.author.guild_permissions.move_member:
                    pass
                else:
                    await ctx.send("```You are not in a voice channel. You must be in a voice channel to use this command.```")
                    return
        vc = nextcord.utils.get(bot.voice_clients, guild=ctx.guild)
        try:
            int(volume)
        except:
            await ctx.send("```Please enter a volume between 0 and 100.```")
        if 0 <= int(volume) <= 100:
            vc.source = nextcord.PCMVolumeTransformer(vc.source)
            vc.source.volume = int(volume)/100
            vc.volume = int(volume)/100
            await ctx.send(f"```Volume set to {volume}%.```")
        else:
            await ctx.send("```Please enter a volume between 0 and 100.```")
    else:
        vc = nextcord.utils.get(bot.voice_clients, guild=ctx.guild)
        if vc:
            await ctx.send(f"```Volume is set to {int(vc.volume*100)}%.```")
        else:
            await ctx.send("```I am not in a voice channel. I must be in a voice channel to use this command.```")


@bot.command(help="Pauses radio playback", aliases=["pause"])
async def tuneout(ctx):
    global song
    global songtime
    if not ctx.voice_client:
        await ctx.send("```I am not in a voice channel. I must be in a voice channel to use this command.```")
        return
    else:
        if ctx.author.voice:
            if (not ctx.author.voice.channel == ctx.voice_client.channel) or not ctx.author.guild_permissions.move_members:
                await ctx.send("```We are not in the same voice channel. We must be in the same voice channel to use this command.```")
                return
            else:
                await ctx.send(f"```Tuning out...```")
        else:
            if ctx.author.guild_permissions.move_member:
                await ctx.send(f"```Tuning out...```")
            else:
                await ctx.send("```You are not in a voice channel. You must be in a voice channel to use this command.```")
                return
    if not ctx.voice_client.is_playing():
        await ctx.send("```I am already paused. The radio must be tuned in for this command to work.```")
    ctx.voice_client.stop()

@bot.command(help="Continues radio playback after pausing", aliases=["resume"])
async def tunein(ctx):
    global song
    global songtime
    if not ctx.voice_client:
        await ctx.send("```I am not in a voice channel. I must be in a voice channel to use this command.```")
        return
    else:
        if ctx.author.voice:
            if (not ctx.author.voice.channel == ctx.voice_client.channel) or not ctx.author.guild_permissions.move_members:
                await ctx.send("```We are not in the same voice channel. We must be in the same voice channel to use this command.```")
                return
            else:
                await ctx.send(f"```Tuning back in...```")
        else:
            if ctx.author.guild_permissions.move_member:
                await ctx.send(f"```Tuning back in...```")
            else:
                await ctx.send("```You are not in a voice channel. You must be in a voice channel to use this command.```")
                return
    if ctx.voice_client.is_playing():
        await ctx.send("```I am still playing. The radio must be tuned out for this command to work.`")
    ctx.voice_client.volume = 1
    source = nextcord.FFmpegPCMAudio(f"assets/audio/sfx/syntheffect1.mp3")
    source.volume = ctx.voice_client.volume
    ctx.voice_client.play(source)
    input_file = f"assets/audio/ost/{song}"
    output_file = f"env/out/{ctx.guild.id}.mp3"
    start_time = round((9 + songtime)* 1000)
    audio = File(f"assets/audio/ost/{song}")
    end_time = round(1000* audio.info.length)
    audio = AudioSegment.from_mp3(input_file)
    sliced_audio = audio[start_time:end_time]
    sliced_audio.export(output_file, format="mp3")
    while True:
        try:
            source = nextcord.FFmpegPCMAudio(f"env/out/{ctx.guild.id}.mp3")
            source.volume = ctx.voice_client.volume
            ctx.voice_client.play(source)
            break
        except:
            await asyncio.sleep(1)
            continue

@bot.command(help="Disonnects the bot from a voice channel", aliases=["disconnect"])
async def leave(ctx):
    if not ctx.voice_client:
        await ctx.send("```I am not in a voice channel. I must be in a voice channel to use this command.```")
    else:
        if ctx.author.voice:
            if ctx.author.voice.channel == ctx.voice_client.channel or ctx.author.guild_permissions.move_members:
                await ctx.send(f"```Leaving {ctx.voice_client.channel}...```")
                await ctx.voice_client.disconnect()
            else:
                await ctx.send("```We are not in the same voice channel. We must be in the same voice channel to use this command.```")
        else:
            if ctx.author.guild_permissions.move_members:
                await ctx.send(f"```Leaving {ctx.voice_client.channel}...```")
                await ctx.voice_client.disconnect()
            else:
                await ctx.send("```You not in a voice channel. You must be in a voice channel to use this command.```")

try:
    bot.run(token)
except Exception as e:
    print(cs(f"[{time.ctime()}] Error: {e}", "red"))