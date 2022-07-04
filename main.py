
import os

import discord
from discord.ext import commands

from keep_alive import keep_alive

bot = commands.Bot(
	command_prefix="!",  
	case_insensitive=True  
)

bot.author_id = 476044993505525780
bot.owner_ids = [476044993505525780, 876187417634291752]

@bot.event 
async def on_ready(): 
    print("I'm in")
    print(bot.user)  

extensions = [
	'cogs.DevCommands',
  'cogs.Greeting',
  'cogs.Dm',
  'cogs.Roles',
]

if __name__ == '__main__':  # Ensures this is the file being ran
	for extension in extensions:
		bot.load_extension(extension)  # Loades every extension.

keep_alive()  # Starts a webserver to be pinged.
token = os.environ.get("DISCORD_BOT_SECRET") 

bot.run(token)  # Starts the bot
