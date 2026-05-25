import nextcord, os, sys, tomllib
sys.dont_write_bytecode = True # I hate __pycache__ files lol.
from nextcord.ext import commands

with open("config.toml", "rb") as config_file:
    config = tomllib.load(config_file)

TOKEN=config["bot"]["token"]
GUILD_ID=config["bot"]["guild_id"]
PREFIX=config["bot"]["prefix"]

client = commands.Bot(
        command_prefix=PREFIX,
        intents=nextcord.Intents.all(),
        default_guild_ids=[GUILD_ID])

for event in os.listdir("events"):
    if event.endswith(".py"):
        client.load_extension(f"events.{event[:-3]}")

for command in os.listdir("commands"):
    if command.endswith(".py"):
        client.load_extension(f"commands.{command[:-3]}")

client.run(TOKEN)
