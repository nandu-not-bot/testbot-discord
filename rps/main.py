import discord
from discord.ext import commands

PURPLE = 0x510490

class RPScog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='rps')
    async def rps(self, ctx):
        p1 = ctx.author
        channel = ctx.channel
        rock_emoji = '👊'
        scissors_emoji = '✌'
        paper_emoji = '✋'

        intro_embed = discord.Embed(
            title=f'So, it is {p1.display_name} vs ME! Let the Game Begin!', 
            description='FYI, the game ends in 5 points.'
            )
        await ctx.reply(embed=intro_embed, mention_author=False)

        p1_score = 0
        ai_score = 0

        def play_check(m):
            return m.content in ['rock', 'paper', 'scissors'] and m.channel == channel and m.author == p1

        import rps.WinLogic as wl

        game_embed = discord.Embed(
            title=f'{p1.display_name.upper()}[{p1_score}] VS CHITTI 😎[{ai_score}]',
            description=f'{p1.display_name}, type your choice! rock, paper or scissors.'
            )
        game_embed.set_footer(text='You can also you "r", "p" and "s". Also type in "end" to end the game.')
        await ctx.send(embed=game_embed)

        while True:            
            pchoice = await self.bot.wait_for('message', check=play_check)
            randchoice = wl.ai_choice()
            outcome = wl.win_logic(randchoice, pchoice.content.lower())[0]
            
            # Decide Emoji
            if pchoice == 'rock':
                p_emoji = rock_emoji
            elif pchoice == 'paper':
                p_emoji = paper_emoji
            elif pchoice == 'scissors':
                p_emoji = scissors_emoji

            if randchoice == 'rock':
                b_emoji = rock_emoji
            elif randchoice == 'paper':
                b_emoji = paper_emoji
            elif randchoice == 'scissors':
                b_emoji = scissors_emoji

            if outcome == 'w':
                play_embed = discord.Embed(title=f'')

            elif outcome == 'l':
                ai_score += 1
                await ctx.send(f'{pchoice.content.upper()}({p1.mention}) **VS** {randchoice.upper()}(BOT))')
                await ctx.send('BOT SCORED! ')
                await ctx.send(f'''`SCORE: {p1_score}(YOU) - {ai_score}(BOT)`''')

            else:
                await ctx.send(f'{pchoice.content.upper()}({p1.mention}) **VS** {randchoice.upper()}(BOT))')
                await ctx.send('IT WAS A DRAW! ')
                await ctx.send(f'''`SCORE: {p1_score}(YOU) - {ai_score}(BOT)`''')

            if ai_score == 5 or p1_score == 5:
                winner = None
                if ai_score > p1_score:
                    winner = 'Bot'
                else:
                    winner = 'You'
                await ctx.send(f'GAME OVER! {winner} won! Final scores: {p1_score} - {ai_score}')
                break


def setup(bot):
    bot.add_cog(RPScog(bot))
