import discord
from discord.ext import commands


class Greeting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('Welcome {0.mention}.'.format(member))
        # if member.guild.id == 707879098984695808:
        #     await member.add_roles(discord.utils.get(member.guild.roles, name="Member"))
        await member.send(f'Welcome to the server, {member.mention}!')

    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send('Hello {0.name}~'.format(member))
        else:
            await ctx.send('Hello {0.name}... This feels familiar.'.format(member))
        self._last_member = member

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        # role, user = self.parse_reaction_payload(payload)
        # if role is not None and user is not None:
            # await user.add_roles(role, reason="ReactionRole")
            print("reaction added")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        # role, user = self.parse_reaction_payload(payload)
        # if role is not None and user is not None:
            print("reaction removed")
            # await user.remove_roles(role, reason="ReactionRole")

def setup(bot):
	bot.add_cog(Greeting(bot))
