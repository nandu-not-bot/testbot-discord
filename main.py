import discord
from discord.ext import commands
import time

def get_prefix(bot, message):
    prefixes = ['do ', '?', '.']

    if not message.guild:
        return '?'

    return commands.when_mentioned_or(*prefixes)(bot, message)


initial_extensions = ['ranking.ranking']
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=get_prefix,
                   description="Just Chillin'!", intents=intents)
bot.remove_command('help')

if __name__ == "__main__":
    for extension in initial_extensions:
        bot.load_extension(extension)

@bot.event
async def on_ready():
    print(
        f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')

    await bot.change_presence(activity=discord.Game(name='My Bot', type=1, url=''))
    print('Successfully logged in and booted...')

bot.run('ODU4NjM1ODY0NzcwMDg0ODg1.YNhA9g.kJxYbLg52yLPHYlI90Qxzx9WXKQ',
        bot=True, reconnect=True)
