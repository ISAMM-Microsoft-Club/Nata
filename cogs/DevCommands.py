import asyncio
import functools

import discord
from discord.ext import commands


class Parent(discord.ui.View):
    """Parent class dedicated to Views"""
    async def on_error(self, interaction: discord.Interaction, error: Exception, item: any):
        interaction.client.dispatch("view_error", interaction, error, item)

class CustomDropdown(discord.ui.Select):
    def __init__(self, placeholder : str, min_val : int, max_val : int, options, when_callback: functools.partial):
        super().__init__(
            placeholder=placeholder,
            min_values=min_val,
            max_values=max_val,
            options = 
                [
                    discord.SelectOption(
                        label=option["label"],
                        description=option.get("description", None),
                        emoji=option.get("emoji", None)
                    ) 
                    for option in options
                ]
        )
        self.when_callback = when_callback

    async def callback(self, interaction: discord.Interaction):
        await self.when_callback(self, interaction)

class dropdown(Parent):
    """Dropdown View"""
    def __init__(self, invoke, placeholder : str, min_val : int, max_val : int, options, when_callback):
        super().__init__()

        self.invoke = invoke

        self.add_item(
            CustomDropdown(
                placeholder=placeholder, 
                min_val=min_val,
                max_val=max_val,
                options=options,
                when_callback=when_callback
            )
        )



class DevCommands(commands.Cog, name='Developer Commands'):
	'''These are the developer commands'''

	def __init__(self, bot):
		self.bot = bot

	async def cog_check(self, ctx):
		return ctx.author.id in self.bot.config.owner_ids

	@commands.command(name="rolesInit", aliases=['ri'], help='Initializes the department roles poll for the server.' ,hidden=True)
	async def roles__init__(self, ctx):
		"""Initializes the department roles poll for the server.
		"""
		channel = discord.utils.get(ctx.guild.channels, name="roles")
		embed = discord.Embed(title="Department Selection", description="React to the emojis corresponding with your department", color=0xE91E63)
		roles_fields = [ f"\n{self.bot.config.roles_init['emojis'][index]} : {self.bot.config.roles_init['department'][index]}\n" for index, value in enumerate(self.bot.config.roles_init["roles"])]
		embed.add_field(name="Departments", value=f"""{"***-***".join(roles_fields)}""")
		message = await channel.send(embed=embed)
		for reaction in self.bot.config.roles_init["emojis"]:
			await message.add_reaction(reaction)


	@commands.command(name="dropdown")
	@commands.guild_only()
	async def dro(self, ctx):
		"""Discover select menu feature with this command."""
		async def when_callback(_class, interaction: discord.Interaction):
			message = "Selected Department : "
			for value in _class.values:
				message += f"`{value}` "
			await interaction.response.send_message(message, ephemeral=True)
			role = ctx.guild.get_role(self.bot.config.roles_init['roles'][self.bot.config.roles_init['department'].index(_class.values[0])])
			await _class.view.invoke.author.add_roles(role)
			await _class.view.invoke.author.remove_roles(ctx.guild.get_role(self.bot.config.no_department))


		roles_fields = [ {"emoji":self.bot.config.roles_init['emojis'][index], "label": self.bot.config.roles_init['department'][index]} for index, value in enumerate(self.bot.config.roles_init["roles"])]

		view = dropdown(invoke=ctx, placeholder="Select your language(s)", min_val=1, max_val=1, options=roles_fields, when_callback=when_callback)
		channel = self.bot.get_channel(self.bot.config.roles_channel)
		await channel.send("Department Selection : ", view=view)


	@commands.command(name="clear", aliases=['cls'], help='Deletes messages from a channel',hidden=True)
	async def clear(self, ctx, limit):
		await self.bot.get_channel(ctx.channel.id).purge(limit=int(limit))
		return

	@commands.command(name="absent", aliases=['irl-abs'], help="Mark the absence of members in irl meeting manually", hidden=True)
	async def absent(self, ctx, *id, severity):
		return 


async def setup(bot):
	await bot.add_cog(DevCommands(bot))
