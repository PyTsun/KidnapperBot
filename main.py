from calendar import month
from discord.ext import commands
import discord
import logging
import random
import json
import os

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix = "k.", case_insensitive=True, intents=intents, owner_ids=[583200866631155714, 801975525060771880])
bot.remove_command("help")
logging.basicConfig(level=logging.INFO)

@bot.event
async def on_ready():
    print("Bot Online!")
    print("Loading Cogs...")
    await bot.load_extension("cogs.commands")
    await bot.load_extension("cogs.handlers")
    print("Done!")

@bot.command()
@commands.is_owner()
async def sync(ctx):
    print("Syncing commands...")
    await bot.tree.sync()
    print("Synced Commands!")

bot.run(os.environ['token'])
