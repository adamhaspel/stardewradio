# IMPORTS
import sys
import os
from dotenv import load_dotenv
from stringcolor import *
import time
import nextcord
from nextcord.ext import commands

# CONSTANTS
TESTING_GUILD_ID = 1386354564441182268

# Checks for arguments
if len(sys.argv) == 1:
    tokentype = input("> ")
else:
    tokentype = sys.argv[1]

# Accessing the token in env and checks if it is available
while True:
    load_dotenv("env/.env")  # Load variables from .env

    # Keep trying until a token is returned
    token = os.getenv(tokentype)
    if token == None:
        tokentype = input(cs(f"[{time.ctime()}] Startup Error: Not a set token", "red") + "\n> ")
        continue
    break
os.system('clear')

# Create bot class
intents = nextcord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="r!", intents=intents)

# Occurs on startup
@bot.event
async def on_connect():
    print(cs(f'[{time.ctime()}] Logging in as {bot.user.name}. Please stand by...', "green"))

# Occurs on connection
@bot.event
async def on_ready():
    print(cs(f'[{time.ctime()}] {bot.user.name} is ready to function.', "green"))

# @bot.slash_command(name="test", help="Shows this message")
# async def test(interaction: nextcord.Interaction):
#     await interaction.send("Hello!")

bot.run(token)