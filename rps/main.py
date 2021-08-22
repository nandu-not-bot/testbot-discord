from discord.ext import commands
import random
from enum import Enum
from rps.logic import logic

class Play(Enum):
    rock = 1
    paper = 2
    scissors = 3

class Outcome(Enum):
    win = 1
    loss = 2
    draw = 3

class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def bot_choice(self):
        return Play(random.randint(1, 3))

    @commands.command()
    async def test(self, ctx):
        await ctx.send(self.bot_choice())

def setup(bot):
    bot.add_cog(Cog(bot))