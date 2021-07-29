import discord
from discord.ext import commands
from discord.ext.commands.context import Context
import json

class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.file = 'ranking/rankings.json'

    def get_data(self):
        with open(self.file, 'r') as f:
            data = json.load(f) 
        return data
    
    def update_data(self, data):
        with open(self.file, 'w') as f:
            json.dump(data, f)

    def reg_member(self, guild, author):
        data = self.get_data()
        data[str(guild.id)][str(author.id)] = {
            'name' : author.name,
            'score' : 0
        }
        self.update_data(data)

    def reg_guild(self, guild, author):
        data = self.get_data()
        guild_id = str(guild.id)
        data[guild_id] = {
            'excluded_channels' : []
        }
        self.update_data(data)
        self.reg_member(guild, author)

    def check_guild(self, guild, author):
        if not author.bot:
            data = self.get_data()

            guild_id = str(guild.id)
            author_id = str(author.id)

            if guild_id in data:
                if author_id not in data[guild_id]:
                    self.reg_member(guild, author)
            elif guild_id not in data:
                self.reg_guild(guild, author)

    def decode_mention(self, mention:str):
        mention = mention.replace('<', '')
        mention = mention.replace('@', '')
        mention = mention.replace('>', '')
        mention = mention.replace('!', '')
        return mention

    def member_exists(self, mention, guild):
        mention = self.decode_mention(mention)
        try: int(mention)
        except: 
            return False 
        
        server = self.bot.get_guild(guild.id)
        if server.get_member(int(mention)) is None:
            return False 

        else:
            member = server.get_member(int(mention))
            data = self.get_data()

            if member not in data[str(guild.id)] and not member.bot:
                self.reg_member(guild, member)
        
        return True
            
    @commands.Cog.listener()
    @commands.guild_only()
    async def on_message(self, message):        
        if message.author.bot: return

        self.check_guild(message.guild, message.author)

        data = self.get_data()

        data[str(message.guild.id)][str(message.author.id)]['name'] = message.author.name
        data[str(message.guild.id)][str(message.author.id)]['score'] += 1

        self.update_data(data)

    @commands.group(name='tier', invoke_without_command=True)
    @commands.guild_only()
    async def tier(self, ctx:Context):
        await ctx.send('Command cannot be invoked without a subcommand. Use `$help tier` for more info.')

    @tier.command()
    async def score(self, ctx:Context, member=None):
        if member is None:
            member = ctx.author
        else:
            if self.member_exists(member, ctx.guild):
                member = ctx.guild.get_member(int(self.decode_mention(member)))
            else:
                await ctx.send(f'Member "{member}" does not exist in this server')

        if member.bot:
            await ctx.send('Doesnt work with bots, mate. :/') 
            return

        self.check_guild(ctx.guild, member)

        embed = discord.Embed(title=member.name)
        data = self.get_data()
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name='Messaging Score', value=f'Your messaging score is `{data[str(ctx.guild.id)][str(member.id)]["score"]}`.')
        await ctx.reply(embed=embed, mention_author=False)

def setup(bot):
    bot.add_cog(Cog(bot))