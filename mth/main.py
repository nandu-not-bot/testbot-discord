from discord.ext import commands
from discord.ext.commands.context import Context

class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def math(self, nums: list, op: str, ctx: Context):
        try: nums = list(map(float, nums))
        except: return f'Input error! Use `{ctx.prefix}help math {ctx.command}` for help.', None

        show = (
            ''.join(f'{x} {op} ' for x in nums)[:-3]
            if op in {'+', '*'}
            else f'{nums[0]} {op} {nums[1]}'
        )

        if op == '*':
            result = 1
            for num in nums:
                result *= num
        elif op == '+':
            result = sum(nums)
        elif op == '-':
            result = nums[0] - nums[1]
        elif op == '/':
            result = nums[0] / nums[1]

        return show, result

    @commands.command()
    async def add(self, ctx: Context, *nums):
        show, result = self.math(nums, '+')
        await ctx.send(f'{show} = {result}' if result is not None else show)    

def setup(bot):
    bot.add_cog(Cog(bot))