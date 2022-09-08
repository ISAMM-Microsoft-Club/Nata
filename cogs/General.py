import discord
from discord.ext import commands


class General(commands.Cog):

  def __init__(self, bot):
      self.bot = bot

  @commands.Cog.listener()
  async def on_message(self, message):
    if any( word in message.content.lower() for word in ['nitro', 'curse']):
      await message.delete()

  @commands.command(name='ping', aliases=['p'], description='Test the Bot\'s latency')
  async def ping(self, ctx):
    await ctx.send(f'Pong! {round(self.bot.latency * 1000)}ms')

  @commands.command(name="args", aliases=['ar'], help="Quotes a list of inputs")
  async def multi_quote(self, ctx, *args):
    one_word_per_line = '\n'.join(args)
    quote_text = 'You said:\n>>> {}'.format(one_word_per_line)
    await ctx.send(quote_text)

async def setup(bot):
	await bot.add_cog(General(bot))
