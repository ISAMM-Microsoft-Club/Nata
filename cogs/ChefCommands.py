
import discord
import requests
from discord.ext import commands

from .Nata.Meet import Meet


class ChefCommands(commands.Cog, name='Developer Commands'):
	'''These are the developer commands'''

	def __init__(self, bot):
		self.bot = bot

	async def cog_check(self, ctx):
		return ctx.author.id in self.bot.chefs_check


	@commands.command(name="meet", aliases=['fm'])
	async def meet(self, ctx, time, link, *args):
		if self.bot.chef_department[str(ctx.author.id)] == "Administration" and not len(args):
			await ctx.send("Please Specify the department (only for administration)")
			embed=discord.Embed(title="Meet Command Example", description="!meet <time> <PV link> <Department>", color=0x00ffff)
			await ctx.send(embed=embed)
			return
		await Meet( self.bot, ctx, time, link, ctx.author.id, args[0]).meet()


def setup(bot):
	bot.add_cog(ChefCommands(bot))
