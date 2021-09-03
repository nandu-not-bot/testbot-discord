import json

import discord
from discord.ext import commands
from discord.ext.commands.context import Context


class Cog(commands.Cog):

    '''Help Cog for chitti'''

    def __init__(self, bot):
        self.bot = bot
        with open("help.json", "r") as file:
            self.data = json.load(file)

    @commands.command(aliases=['h'])
    async def help(self, ctx: Context, command: str = None):
        if command is None or command not in self.data["commands"]:
            embed = discord.Embed(
                title = 'Help command for chitti'.title(),
                description = f'Enter `{ctx.prefix}help <command>` (without "<>") for more info on the command.',
                color=0xB26EfA
            )
            for group in self.data["groups"]:
                embed.add_field(
                    name = group,
                    value= ''.join(self.data["groups"][group])
                )

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Cog(bot))