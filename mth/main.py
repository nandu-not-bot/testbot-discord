from discord.ext import commands
from discord.ext.commands.context import Context

class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add(self, ctx: Context, *nums):
        try:
            nums = list(map(float, nums))
        except:
            await ctx.send(f'Input error! use `{ctx.prefix}help math {ctx.command}`')
            return

        show = ''.join(f'{x} + ' for x in nums)
        
        await ctx.send(f'{show[:-2]} = {sum(nums)}')

def setup(bot):
    bot.add_cog(Cog(bot))