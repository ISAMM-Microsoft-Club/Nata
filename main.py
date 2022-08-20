
import json
import os

import discord
from discord.ext import commands


async def cogs_manager(bot: commands.Bot, mode: str, cogs: list) -> None:
  for cog in cogs:
    try:
      await bot.load_extension(cog)
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

    cogs = [
      'cogs.DevCommands',
      'cogs.Greeting',
      'cogs.Dm',
      'cogs.Roles',
      'cogs.General',
      'cogs.ChefCommands',
      'cogs.ErrorHandling',
      'cogs.Help'
    ]
    await cogs_manager(self, "load", cogs)
    self.loop.create_task(self.startup())


class Config:
  def __init__(self):
    self.author_id = 476044993505525780
    with open("./__Data.json") as data:
      Variables = json.load(data)
      self.owner_ids = Variables["owner_ids"]
      self.roles_channel = Variables['channels']["roles_channel"]
      self.real_name_channel = Variables['channels']["real_name_channel"]
      self.chefs_check = [int(id) for id in list(Variables["chefs"].keys())]
      self.new_member_role = Variables["roles"]["newmember"]
      self.member_role = Variables["roles"]["member"]
      self.no_department = Variables["roles"]["no_department"]
      self.welcome_channel = Variables['channels']["welcome_channel"]
      self.chefs = Variables["chefs"]
      self.chef_department = { chef:Variables['chefs'][str(chef)]['department'] for chef in Variables["chefs"]}
      self.roles_init = Variables["roles"]["roles_init"]


if __name__ == '__main__':

  bot = Bot()
  bot.config = Config()

  bot.run(
    os.environ.get("DISCORD_BOT_SECRET"),
    reconnect=True,
  )
