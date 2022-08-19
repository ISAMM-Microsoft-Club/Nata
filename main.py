
import json
import os

import discord
from discord.ext import commands


async def cogs_manager(bot: commands.Bot, mode: str, cogs: list) -> None:
  for cog in cogs:
    try:
      if mode == "unload":
        await bot.unload_extension(cog)
      elif mode == "load":
        await bot.load_extension(cog)
      elif mode == "reload":
        await bot.reload_extension(cog)
      else:
        raise ValueError("Invalid mode.")
    except Exception as e:
      raise e

class Bot(commands.Bot):
  def __init__(self):
    super().__init__(
      allowed_mentions=discord.AllowedMentions(everyone=False),
      case_insensitive = True,
      command_prefix = '!',
      intents = discord.Intents.all(),
      max_messages=2500
    )

  async def on_ready(self):
    print(f'{self.user} has connected to Discord!')

  async def close(self):
    print(f'{self.user} has disconnected from Discord!')


  async def startup(self):
    """Sync application commands"""
    await self.wait_until_ready()

    await self.tree.sync()

  async def setup_hook(self):
    """Initialize the db, prefixes & cogs."""


    # Cogs loader
    cogs = [
      'cogs.DevCommands',
      'cogs.Greeting',
      'cogs.Dm',
      'cogs.Roles',
      'cogs.General',
      'cogs.ChefCommands',
      'cogs.ErrorHandling',
    ]



    await cogs_manager(self, "load", cogs)

    # Sync application commands
    self.loop.create_task(self.startup())



if __name__ == '__main__':

  bot = Bot()

  bot.author_id = 476044993505525780
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
  bot.run(
    os.environ.get("DISCORD_BOT_SECRET"),
    reconnect=True,
  )
