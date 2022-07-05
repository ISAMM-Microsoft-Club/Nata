import discord
from discord.ext import commands


class General(commands.Cog):

  def __init__(self, bot):
      self.bot = bot

  @commands.Cog.listener()
  async def on_message(self, message):
    if any( word in message.content.lower() for word in ['nitro', 'curse']):
      await message.delete()



def setup(bot):
	bot.add_cog(General(bot))
