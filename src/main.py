import sys
import os
from dotenv import load_dotenv
from stringcolor import *
import time
import nextcord
from nextcord.ext import commands

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
bot = commands.Bot(command_prefix="r!", intents=intents,activity = nextcord.Activity(name="r!help", type=2))

@bot.event
async def on_connect():
    print(cs(f'[{time.ctime()}] Info: Logging in as {bot.user.name}. Please stand by...', "green"))

@bot.event
async def on_ready():
    print(cs(f'[{time.ctime()}] Info: {bot.user.name} is ready to function.', "green"))

@bot.event
async def on_disconnect():
    print(cs(f'[{time.ctime()}] Info: Disconnecting from {bot.user.name}. Please stand by...', "green"))

@bot.event
async def on_close():
    print(cs(f'\r[{time.ctime()}] Info: {bot.user.name} is logging off.', "green"))

@bot.command(help="Connects the bot to a voice channel", aliases=["connect"])
async def join(ctx):
    if not ctx.author.voice:
        await ctx.send("```You are not in a voice channel. You must be in a voice channel to use this command.```")
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