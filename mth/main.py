from discord.ext import commands
from discord.ext.commands.context import Context

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

    @commands.command()
    async def mean(self, ctx: Context, *nums):
    
        '''Gives the arithmetic mean or average of an infinite number of given numbers.'''
    
        try:
            nums = list(map(float, nums))
        except:
            await ctx.send(f'Input error! Use `{ctx.prefix}help math {ctx.command}` for help.') 
            return

        mean = sum(nums) / len(nums)

        await ctx.send(f'The arithmetic mean of `{nums}` is `{mean}`')

    @commands.command()
    async def median(self, ctx: Context, *nums):
    
        '''Gives the mdian of an infinite list of given numbers.'''
    
        try:
            nums = list(map(float, nums))
        except:
            await ctx.send(f'Input error! Use `{ctx.prefix}help math {ctx.command}` for help.')
            return

        nums.sort()

        median = nums[((len(nums) + 1) / 2) + 1] if len(nums) % 2 == 0 else (nums[((len(nums) + 1) / 2) + 1] + nums[(len(nums) / 2) + 1]) / 2

        await ctx.send(f'The median of `{nums}` is `{median}`')

    @commands.command()
    async def mode(self, ctx: Context, *nums):
    
        '''Gives the mode of an infinite list of given numbers.'''
    
        try:
            nums = list(map(float, nums))
        except:
            await ctx.send(f'Input error! Use `{ctx.prefix}help math {ctx.command}` for help.')
            return

        uniques = set(nums)

        modes = []
        top_count = 0

        for num in uniques:
            count = nums.count(num)
            if count == top_count:
                modes.append(nums)

            elif count > top_count:
                modes = [nums]
                top_count = count

        await ctx.send(f'The mode(s) of the list `{nums}` is `{modes if len(modes) > 1 else modes[0]}` occuring `{count}` number of times each.')

def setup(bot):
    bot.add_cog(Cog(bot))