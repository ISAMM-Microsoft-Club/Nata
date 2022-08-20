
import discord
import requests
from discord.ext import commands

from .Schedule.Meet import Meet


class ChefCommands(commands.Cog, name='Chef Commands', description='Chef Commands'):
	'''These are the developer commands'''

	def __init__(self, bot):
		self.bot = bot

	async def cog_check(self, ctx):
		return ctx.author.id in self.bot.config.chefs_check


	@commands.command(name="meet", aliases=['fm'], help="Schedule a meet", hidden=True)
	async def meet(self, ctx, time, link, *args):
		if self.bot.config.chef_department[str(ctx.author.id)] == "Administration" and not len(args):
			await ctx.send("Please Specify the department (only for administration)")
			embed=discord.Embed(title="Meet Command Example", description="!meet <time> <PV link> <Department>", color=0x00ffff)
			await ctx.send(embed=embed)
			return
		dept = args[0] if len(args) else self.bot.config.chef_department[str(ctx.author.id)]
		await Meet( self.bot, ctx, time, link, ctx.author.id, dept).meet()

	@meet.error
	async def do_repeat_handler(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send("You forgot to give an argument!")
			embed=discord.Embed(title="Meet Command Example", description="!meet <time> <PV link> <Department>", color=0x00ffff)
			await ctx.send(embed=embed)
		else:
			await ctx.send(error)

async def setup(bot):
	await bot.add_cog(ChefCommands(bot))

