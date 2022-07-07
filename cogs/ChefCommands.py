import discord
import requests
from discord.ext import commands

from .Nata.Formation import Formation


class ChefCommands(commands.Cog, name='Developer Commands'):
	'''These are the developer commands'''

	def __init__(self, bot):
		self.bot = bot

	async def cog_check(self, ctx):
		return ctx.author.id in self.bot.chefs_check


	@commands.command(name="formation", aliases=['fm'])
	async def formation(self, ctx, time):
		await Formation( self.bot, ctx, time, ctx.author.id).confirmation()


	@commands.command(name="formation_pv", aliases=['fmpv'])
	async def upload_file(self, ctx):
		attachment_url = ctx.message.attachments[0].url
		file_request = requests.get(attachment_url)
		await ctx.send(file_request.content)

def setup(bot):
	bot.add_cog(ChefCommands(bot))
