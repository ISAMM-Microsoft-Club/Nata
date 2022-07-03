import discord
from discord.ext import commands

from .Nata.Formation import Formation


class DevCommands(commands.Cog, name='Developer Commands'):
	'''These are the developer commands'''

	def __init__(self, bot):
		self.bot = bot

	async def cog_check(self, ctx):  
		'''
		The default check for this cog whenever a command is used. Returns True if the command is allowed.
		'''
		return ctx.author.id in self.bot.owner_ids

	@commands.command(name="listcogs", aliases=['lc'])
	async def listcogs(self, ctx):
		'''
		Returns a list of all enabled commands.
		'''
		base_string = "```css\n"
		base_string += "\n".join([str(cog) for cog in self.bot.extensions])
		base_string += "\n```";  print(base_string)
		await ctx.send(base_string)

	@commands.command(name="args", aliases=['ar'], hidden=True)
	async def multi_quote(self, ctx, *args):
			one_word_per_line = '\n'.join(args)
			quote_text = 'You said:\n>>> {}'.format(one_word_per_line)
			await ctx.send(quote_text)


	@commands.command(name="formation", aliases=['fm'])
	async def formation(self, ctx, time):
		frm = Formation( self.bot, ctx, time, ctx.author.id)
		await frm.confirmation()

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.author == self.bot.user:
			return
		if any(word in message.content.lower() for word in ['nitro', 'curse2']):
			await message.delete()

def setup(bot):
	bot.add_cog(DevCommands(bot))
