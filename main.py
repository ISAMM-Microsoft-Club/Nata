
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


with open("./__Data.json") as data:
  Variables = json.load(data)
  bot.owner_ids = Variables["owner_ids"]
  bot.roles_channel = Variables["roles_channel"]
  bot.reactions = Variables["roles"]["emojis"]
  bot.roles = Variables["roles"]["roles"]
  bot.real_name_channel = Variables["real_name_channel"]
  bot.chefs_check = [int(id) for id in list(Variables["chefs"].keys())]
  bot.chefs = Variables["chefs"]
  bot.chef_department = Variables["chef_department"]
  bot.new_member_role = Variables["roles"]["newmember"]
  bot.member_role = Variables["roles"]["member"]
  bot.no_department = Variables["roles"]["no_department"]
  bot.welcome_channel = Variables["welcome_channel"]

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
  'cogs.ErrorHandling',
]

if __name__ == '__main__':
	for extension in extensions:
		bot.load_extension(extension)

keep_alive()
token = os.environ.get("DISCORD_BOT_SECRET")

bot.run(token)
