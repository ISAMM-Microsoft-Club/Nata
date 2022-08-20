import discord
from discord.ext import commands


class Greeting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None


    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        member = member or ctx.author
        if member.id in self.bot.config.chefs_check:
            await ctx.send(f"Hello {self.bot.config.chefs[str(member.id)]['position']} {member.nick or member.name}!")
        else :
            if self._last_member is None or self._last_member.id != member.id:
                await ctx.send('Hello {}~'.format(member.nick))
            else:
                await ctx.send('Hello {}... This feels familiar.'.format(member.nick))
            self._last_member = member


async def setup(bot):
	await bot.add_cog(Greeting(bot))
