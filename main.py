import os

import disnake
from disnake.ext import commands
from dotenv import load_dotenv

from cogs import DrinkTrackerCog
from drink_db import Drinks

# bot initialization
command_sync_flags = commands.CommandSyncFlags.default()
command_sync_flags.sync_commands_debug = True

intents = disnake.Intents.default()
intents.members = True

bot = commands.InteractionBot(
    command_sync_flags=command_sync_flags,
    intents=intents,
)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}! (ID: {bot.user.id})\n-------")

if __name__ == "__main__":
    load_dotenv()
    bot_token = os.getenv("DISCORD_TOKEN")
    tinydb_path = os.getenv("TINYDB_PATH")

    drink_db = Drinks(tinydb_path)
    bot.add_cog(DrinkTrackerCog(bot, drink_db))
    bot.run(bot_token)