from discord.ext import commands
from discord.ext.commands.context import Context

class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def math(self, nums: list, op: str):
        try: nums = list(map(float, nums))
        except: raise TypeError

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


    # @commands.command()
    # async def add(self, ctx: Context, *nums):
    #     try:
    #         show, result = self.math(nums, '+')
    #         await ctx.send(f'{show} = {result}')
    #     except:
    #         await ctx.send

    async def test_def(self, ctx: Context):
        await ctx.send('tested')

    @commands.command()
    async def test(self, ctx: Context):
        self.test_def(ctx)

def setup(bot):
    bot.add_cog(Cog(bot))