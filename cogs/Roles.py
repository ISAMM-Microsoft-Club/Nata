import discord
from discord.ext import commands


class Greeting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):  
        '''
        The default check for this cog whenever a command is used. Returns True if the command is allowed.
        '''
        return ctx.author.id in self.bot.owner_ids

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):

        # await user.add_roles(role, reason="ReactionRole")
        print("reaction added")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        # role, user = self.parse_reaction_payload(payload)
        # if role is not None and user is not None:
            print("reaction removed")
            # await user.remove_roles(role, reason="ReactionRole")

    # def parse_payload(self, payload: discord.RawReactionActionEvent):
    #     user_id, 
    @commands.command(name="rolesInit", aliases=['ri'])
    async def check_if_message_exists(self, ctx):
        channel = discord.utils.get(ctx.guild.channels, name="roles")
        # message = await channel.history(limit=10).flatten()[0]
        embed = discord.Embed(title="Product Select", description="React to the emojis corresponding with what you need", color=0xE91E63)
        embed.add_field(name="test", value="""
                        :white_check_mark: :    big data
                        ***-***
                        :heart: :    immmmm
                        ***-***
                        :x: :    cmmmmm
                        """)
        message = await channel.send(embed=embed)
        await message.add_reaction("✅")
        await message.add_reaction("❤️")
        await message.add_reaction("❌")
        # await message.add_reaction(":x:")
        # await message.add_reaction(":heart:")
        # await channel.send("Hello") if not channel.history else print("it's there")


    def check_reaction_channel(self, channel: discord.TextChannel):
        return channel.id == 707879098984695808

    #     return role, user
def setup(bot):
	bot.add_cog(Greeting(bot))
