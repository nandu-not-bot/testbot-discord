from discord.ext import commands
import json

class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.file = 'ranking/rankings.json'

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_message(self, message):
        guild = str(message.guild.id)
        author = message.author

        if message.author.bot:
            return

        with open(self.file, 'r') as f:
            data = json.load(f)
        
        if guild in data:
            if str(author.id) in data[guild]:
                data[guild][str(author.id)]['name'] = author.name
                data[guild][str(author.id)]['score'] += 1
            elif str(author.id) not in data[guild]:
                data[guild][str(author.id)] = {
                    'name' : author.name,
                    'score' : 0
                }

        elif guild not in data:
            data[guild] = {
                str(author.id) : {
                    'name' : author.name,
                    'score' : 0
                }
            }

        with open(self.file, 'w') as f:
            json.dump(data, f)

        print(data)



def setup(bot):
    bot.add_cog(Cog(bot))