import discord
from discord import RawReactionActionEvent
from discord.ext import commands
from discord.utils import get


class Roles(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        await member.add_roles(member.guild.get_role(994516549689950268))

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.id == self.bot.user.id:
            return
        if message.channel.id == self.bot.real_name_channel:
            msg = await message.reply(f'{message.author.mention} logged in as {message.content} (react with ❤ to confirm)')
            await msg.add_reaction('❤')


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.user_id == self.bot.user.id:
            return

        if payload.channel_id == self.bot.real_name_channel:
            if payload.emoji.name != '❤' :
                return
            message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
            if str(payload.member.id) in message.content:

                await payload.member.add_roles(message.guild.get_role(994513081432551485))
                await payload.member.remove_roles(message.guild.get_role(994516549689950268))
                client_message = await self.bot.get_channel(payload.channel_id).fetch_message(message.reference.message_id)
                await client_message.reply(f'enjoy your stay {client_message.content}!')

        if payload.channel_id == self.bot.roles_channel_id:

            user_id, role = self.parse_payload(payload)
            print(f"reaction added by {user_id} for {role} ")
            if role in self.bot.reactions:
                server = self.bot.get_guild(payload.guild_id)
                role = server.get_role(self.bot.roles[self.bot.reactions.index(role)])
                user = server.get_member(user_id)
                await user.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        if payload.channel_id != self.bot.roles_channel_id or payload.user_id == self.bot.user.id:
            return
        user_id, role = self.parse_payload(payload)
        print(f"reaction REMOVED by {user_id} for {role} ")
        if role in self.bot.reactions:
            server = self.bot.get_guild(payload.guild_id)
            role = server.get_role(self.bot.roles[self.bot.reactions.index(role)])
            user = server.get_member(user_id)
            await user.remove_roles(role)


    def parse_payload(self, payload: RawReactionActionEvent):
        return payload.user_id, payload.emoji.name







def setup(bot):
    bot.add_cog(Roles(bot))
