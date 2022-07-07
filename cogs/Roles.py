import discord
from discord import RawReactionActionEvent
from discord.ext import commands
from discord.utils import get


class Roles(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        await member.add_roles(member.guild.get_role(self.bot.new_member_role))
        real_name_channel = self.bot.get_channel(self.bot.real_name_channel)
        await real_name_channel.send(f"{member.mention} Please enter your real name here.")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.id == self.bot.user.id:
            return
        if message.channel.id == self.bot.real_name_channel:
            msg = await message.reply(f'{message.author.name} logged in as {message.content} (react with ❤ to confirm)')
            await msg.add_reaction('❤')


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.user_id == self.bot.user.id:
            return

        if payload.channel_id == self.bot.real_name_channel:
            if payload.emoji.name != '❤' :
                return
            message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
            client_message = await self.bot.get_channel(payload.channel_id).fetch_message(message.reference.message_id)
            if payload.member.id == client_message.author.id:
                await client_message.reply(f'enjoy your stay {client_message.content}!')
                discord_user = str(payload.member.name)
                await payload.member.edit(nick=client_message.content)
                await payload.member.add_roles(message.guild.get_role(self.bot.member_role))
                await payload.member.remove_roles(message.guild.get_role(self.bot.new_member_role))
                print(f'Nickname was changed for {discord_user} of id {payload.member.id} to {client_message.content} ')

        if payload.channel_id == self.bot.roles_channel:

            user_id, role = self.parse_payload(payload)
            print(f"reaction added by {user_id} for {role} ")
            if role in self.bot.reactions:
                guild = self.bot.get_guild(payload.guild_id)
                role = guild.get_role(self.bot.roles[self.bot.reactions.index(role)])
                await payload.member.add_roles(role)
                await payload.member.remove_roles(guild.get_role(self.bot.no_role))

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        if payload.channel_id != self.bot.roles_channel or payload.user_id == self.bot.user.id:
            return
        user_id, role = self.parse_payload(payload)
        print(f"reaction REMOVED by {user_id} for {role} ")
        if role in self.bot.reactions:
            guild = self.bot.get_guild(payload.guild_id)
            role = guild.get_role(self.bot.roles[self.bot.reactions.index(role)])
            member = guild.get_member(user_id)
            await member.remove_roles(role)
            await member.add_roles(guild.get_role(self.bot.no_role))

    def parse_payload(self, payload: RawReactionActionEvent):
        return payload.user_id, payload.emoji.name




def setup(bot):
    bot.add_cog(Roles(bot))
