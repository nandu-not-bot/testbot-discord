import discord
from discord.ext import commands
from discord.ext.commands.context import Context
from googletrans import Translator

class Cog(commands.Cog):

    """Translate Cog"""

    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Cog(bot))
