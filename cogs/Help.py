from datetime import datetime, timedelta

import discord
from discord import app_commands
from discord.ext import commands

# from views import help as vhelp


class HelpCommand(commands.HelpCommand):
    """Help command"""

    privlaged_members = [876187417634291752, 476044993505525780, 699990903477108786, 227121772779143179, 374319257976176671, 784376469371093003, 771438796372967424, 583802100337606677]

    async def on_help_command_error(self, ctx, error):
        handledErrors = [
            commands.CommandOnCooldown,
            commands.CommandNotFound
        ]

        if not type(error) in handledErrors:
            print("! Help command Error :", error, type(error), type(error).__name__)
            return await super().on_help_command_error(ctx, error)

    def command_not_found(self, string):
        raise commands.CommandNotFound(f"Command {string} is not found")

    async def send_bot_help(self, mapping):
        commands = []
        hidden_commands = []
        # if self.context.message.author.id in self.bot.config.privladged:
        #     pass


        print()
        for cog in mapping:
            if cog:
                for command in cog.get_commands():
                    if not command.hidden:
                        commands.append(command.name)
                    else :
                        hidden_commands.append(command.name)

        embed = discord.Embed(color=discord.Color.dark_grey(), title = "👋 Help · Home", description = f"Welcome to the help page.\n\nUse `!help command` for more info on a command.\n\u200b")
        commands = "\n".join(commands)
        hidden_commands = "\n".join(hidden_commands)
        embed.add_field(name="Commands", value=f'{commands}\n\u200b', inline=False)
        if self.context.message.author.id in self.privlaged_members:
            print("private")
            #!! Don't forhet to update this
                # if self.context.channel.id != 1010317036284551349:
                #     warning = discord.Embed(color=discord.Color.dark_red(), title = "Warning", description = f"Private commands can't be shared in public channels!")
                #     await self.context.send(embed=warning)
                #     return
            embed.add_field(name="Private Commands", value=f'{hidden_commands}\n\n\u200b', inline=False)
            embed.add_field(name="Who am I ?", value="I'm Nata made by [a group of developers](https://github.com/ISAMM-Microsoft-Club/Nata/graphs/contributors) in Isamm Microsoft Club in 2022.\nI'm open source, you can see my code on [Github](https://github.com/ISAMM-Microsoft-Club/Nata) !")
            await self.context.send(embed = embed, delete_after=120)
            return
        embed.add_field(name="Who am I ?", value="I'm Nata made by [a group of developers](https://github.com/ISAMM-Microsoft-Club/Nata/graphs/contributors) in Isamm Microsoft Club in 2022.\nI'm open source, you can see my code on [Github](https://github.com/ISAMM-Microsoft-Club/Nata) !")
        await self.context.send(embed = embed, delete_after=120)

    async def send_command_help(self, command):
        embed = discord.Embed(title = f"Help : {command.name}", description=f"**Command** : {command.name}\n{command.help}")
        params = ""
        for param in command.clean_params:
            params += f" <{param}>"
        embed.add_field(name="Usage", value=f"!{command.name}{params}", inline=False)
        if len(command.aliases):
          embed.add_field(name="Aliases", value=f"`{command.aliases}`")
        embed.set_footer(text="Remind : Hooks such as <> must not be used when executing commands.", icon_url=self.context.message.author.display_avatar.url)
        await self.context.send(embed=embed)

@app_commands.guild_only()
class Help(commands.Cog, name="help"):
    def __init__(self, bot) -> None:
        self._original_help_command = bot.help_command

        attributes = {
            'name': "help",
            'aliases': ['h', '?']
        }

        bot.help_command = HelpCommand(command_attrs=attributes)



async def setup(bot):
  await bot.add_cog(Help(bot))
