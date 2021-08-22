from discord.ext import commands
from discord.ext.commands.context import Context
import math, statistics

class Cog(commands.Cog):

    '''Simple math commands.'''

    def __init__(self, bot):
        self.bot = bot
        
    def math(self, nums: list, op: str, ctx: Context):
        try: 
            nums = list(map(float, nums))
        except: 
            return f'Input error! Use `{ctx.prefix}help math {ctx.command}` for help.', None

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

    def convert_list(self, input: list):
        input = list(map(float, input))

    # Basic Arithmetic Operations

    @commands.command()
    async def add(self, ctx: Context, *nums):

        '''Gives the sum of an infinite number given numbers.'''

        show, result = self.math(nums, '+', ctx)
        await ctx.send(f'{show} = {result}' if result is not None else show)  

    @commands.command()
    async def sub(self, ctx: Context, *nums):

        '''Gives the differenc of two given numbers.'''

        show, result = self.math(nums, '-', ctx)
        await ctx.send(f'{show} = {result}' if result is not None else show)

    @commands.command()
    async def mult(self, ctx: Context, *nums):

        '''Gives the product of an infinite number of given numbers.'''

        show, result = self.math(nums, '*', ctx)
        await ctx.send(f'{show} = {result}' if result is not None else show)   
    
    @commands.command()
    async def div(self, ctx: Context, *nums):

        '''Gives the quotient of two given numbers.'''

        show, result = self.math(nums, '/', ctx)
        await ctx.send(f'{show} = {result}' if result is not None else show)

    # Statistical Measures of Central Tendancies
    async def convert_list(self, input_list: list, ctx: Context):
        channel = self.bot.get_channel(ctx.channel.id)
        
        await channel.send('tested')

    @commands.command()
    async def mean(self, ctx: Context, *nums):
    
        '''Gives the arithmetic mean or average of an infinite number of given numbers.'''
    
        try:
            nums = list(map(float, nums))
        except:
            await ctx.send(f'Input error! Use `{ctx.prefix}help math {ctx.command}` for help.') 
            return

        mean = statistics.mean(nums)

        await ctx.send(f'The arithmetic mean of `{nums}` is `{mean}`')

    @commands.command()
    async def median(self, ctx: Context, *nums):
    
        '''Gives the mdian of an infinite list of given numbers.'''
    
        try:
            nums = list(map(float, nums))
        except:
            await ctx.send(f'Input error! Use `{ctx.prefix}help math {ctx.command}` for help.')
            return

        median = statistics.median(nums)

        nums.sort()

        await ctx.send(f'The median of `{nums}` is `{median}`')

    @commands.command()
    async def mode(self, ctx: Context, *nums):
    
        '''Gives the mode of an infinite list of given numbers.'''
    
        try:
            nums = list(map(float, nums))
        except:
            await ctx.send(f'Input error! Use `{ctx.prefix}help math {ctx.command}` for help.')
            return

        mode = statistics.mode(nums)

        await ctx.send(f'The mode of the list `{nums}` is `{mode}` occuring `{nums.count(mode)}` number of times.')

    @commands.command()
    async def test(self, ctx: Context):
    
        '''test'''
    
        self.convert_list([], ctx)
    


def setup(bot):
    bot.add_cog(Cog(bot))