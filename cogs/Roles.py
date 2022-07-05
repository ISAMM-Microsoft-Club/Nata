import discord
from discord import PartialEmoji, RawReactionActionEvent
from discord.ext import commands
from discord.utils import get


class Roles(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return ctx.channel.id == self.bot.data["roles_channel"]

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.channel_id != 993567548605989054 or payload.user_id == self.bot.user.id:
            return

        user_id, role = self.parse_payload(payload)
        print(f"reaction added by {user_id} for {role} ")
        reactions = ["❌", "✅", "❤️"]
        roles = [993966213535367188, 993938327294201976, 993938357384130701]
        if role in reactions:
            server = self.bot.get_guild(payload.guild_id)
            role = server.get_role(roles[reactions.index(role)])
            user = server.get_member(user_id)
            await user.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        user_id, role = self.parse_payload(payload)
        print(f"reaction REMOVED by {user_id} for {role} ")
        reactions = ["❌", "✅", "❤️"]
        roles = [993966213535367188, 993938327294201976, 993938357384130701]
        if role in reactions:
            server = self.bot.get_guild(payload.guild_id)
            role = server.get_role(roles[reactions.index(role)])
            user = server.get_member(user_id)
            await user.remove_roles(role)


    def parse_payload(self, payload: RawReactionActionEvent):
        return payload.user_id, payload.emoji.name







def setup(bot):
	bot.add_cog(Roles(bot))
