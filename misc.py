from discord.ext import commands

def get_kwargs(func: callable):
    async def wrapper(self, ctx, *args):
        # $command -a arg -b arg -c arg
        string = " ".join(args)
        args = string.split("-")

        kwargs = {arg[0]: arg[1:] for arg in args}
        await func(self, ctx, kwargs)

    return wrapper

class MiscCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="coolbot")
    async def coolbot(self, ctx):
        await ctx.send("This bot is cool. :)")

    @commands.command()
    async def feedback(self, ctx: commands.context.Context, *feedback):

        """Get feedback from the users"""

        if len(feedback) == 0:
            await ctx.send(
                "❌ Oops! I think you forgot to give your feedback!", delete_after=5
            )
            return

        dev = self.bot.get_user(591078175778537512)
        feedback = "".join(f"{word} " for word in feedback)

        await dev.send(f"**{ctx.author.display_name}** from **{ctx.guild.name}** says: " + feedback)
        await ctx.reply(
            "Team Chitti thanks you for your valuable feedback! 😄", delete_after=30
        )

    @commands.command()
    async def ping(self, ctx):
    
        '''Ping latency'''
    
        await ctx.send(f'I am speed! `{round(self.bot.latency*1000, 1)} ms`')

    @commands.command(name="echo")
    @get_kwargs
    async def echo(self, ctx, kwargs: dict):
        display = "".join(f'{arg}: {value}' for arg, value in kwargs.items())
        await ctx.send(display)

def setup(bot):
    bot.add_cog(MiscCommands(bot))
