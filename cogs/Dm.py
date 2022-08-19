import discord
from discord.ext import commands
from discord.utils import get


class Dm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_message(self, message):
      if message.author == self.bot.user:
        return

      if isinstance(message.channel, discord.channel.DMChannel):
        print(message.author.name)
        await message.channel.send(f'Hello {message.author.name}!')


async def setup(bot):
	await bot.add_cog(Dm(bot))
