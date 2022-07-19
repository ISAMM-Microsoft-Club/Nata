import discord
from discord import RawReactionActionEvent
from discord.ext import commands
from discord.utils import get


class Roles(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.boilerplate = {}

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        await member.add_roles(member.guild.get_role(self.bot.new_member_role))
        real_name_channel = self.bot.get_channel(self.bot.real_name_channel)
        msg = await real_name_channel.send(f"{member.mention} Please enter your real name here.")
        self.boilerplate[str(member.id)] = msg.id

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.id == self.bot.user.id:
            return
        if message.channel.id == self.bot.real_name_channel:
            if message.content == 'clear':
                await self.bot.get_channel(message.channel.id).purge(limit=100)
                print('purged')
                return
            msg = await message.reply(f'{message.author} logged in as {message.content} (react with ❤ to confirm)')
            await msg.add_reaction('❤')
            previous = await message.channel.fetch_message(self.boilerplate[str(message.author.id)])
            await previous.delete()
            self.boilerplate[str(message.author.id)] = msg.id


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.user_id == self.bot.user.id:
            return

        if payload.channel_id == self.bot.real_name_channel:
            if payload.emoji.name != '❤' :
                return
            channel = self.bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            client_message = await channel.fetch_message(message.reference.message_id)
            if payload.member.id == client_message.author.id:
                msg = await client_message.reply(f'enjoy your stay {client_message.content}!')
                await payload.member.edit(nick=client_message.content)
                await payload.member.add_roles(message.guild.get_role(self.bot.member_role))
                await self.bot.get_channel(self.bot.welcome_channel).send(f'{payload.member.mention} 3aslema ya 7mema!')
                await payload.member.add_roles(message.guild.get_role(self.bot.no_department))
                await payload.member.remove_roles(message.guild.get_role(self.bot.new_member_role))
                print(f'Nickname was changed for {payload.member} to {client_message.content} ')
                await client_message.delete()
                await msg.delete()
                msg = await channel.fetch_message(self.boilerplate[str(payload.member.id)])
                await msg.delete()

        if payload.channel_id == self.bot.roles_channel:

            user_id, role = self.parse_payload(payload)
            print(f"reaction added by {user_id} for {role} ")
            if role in self.bot.reactions:
                guild = self.bot.get_guild(payload.guild_id)
                role = guild.get_role(self.bot.roles[self.bot.reactions.index(role)])
                await payload.member.add_roles(role)
                await payload.member.remove_roles(guild.get_role(self.bot.no_department))

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
            await member.add_roles(guild.get_role(self.bot.no_department))

    def parse_payload(self, payload: RawReactionActionEvent):
        return payload.user_id, payload.emoji.name




def setup(bot):
    bot.add_cog(Roles(bot))

