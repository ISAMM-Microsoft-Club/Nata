
import json
import os

import discord
from discord.ext import commands

from keep_alive import keep_alive

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(
	command_prefix="!",  
	case_insensitive=True ,
  intents=intents
)


with open("./Data.json") as data:
  Variables = json.load(data)
  bot.owner_ids = Variables["owner_ids"]
  bot.roles_channel = Variables["roles_channel"]
  bot.reactions = Variables["roles"]["emojis"]
  bot.roles = Variables["roles"]["roles"]
  bot.real_name_channel = Variables["real_name_channel"]
  bot.chefs = Variables["chefs"]
  bot.new_member_role = Variables["roles"]["newmember"]
  bot.member_role = Variables["roles"]["member"]

bot.author_id = 476044993505525780

@bot.event 
async def on_ready(): 
    print("I'm in")
    print(bot.user)  

extensions = [
	'cogs.DevCommands',
  'cogs.Greeting',
  'cogs.Dm',
  'cogs.Roles',
  'cogs.General',
  'cogs.ChefCommands',
]

if __name__ == '__main__':  # Ensures this is the file being ran
	for extension in extensions:
		bot.load_extension(extension)  # Loades every extension.

keep_alive()  # Starts a webserver to be pinged.
token = os.environ.get("DISCORD_BOT_SECRET") 

bot.run(token)  # Starts the bot
