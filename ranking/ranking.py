from os import name
import discord
from discord.ext import commands
from discord.ext.commands.context import Context
import json

PURPLE = 0x510490

class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.file = 'ranking/rankings.json'
    
    def sort_members(self, members):
        sorted_list = []
        for member in members:
            def check():
                for x in sorted_list:
                    last = len(sorted_list)-1
                    if member[1] <= x[1]:
                        return (True, sorted_list.index(x))
                    elif member[1] >= sorted_list[last][1] and x[1] == sorted_list[last][1]:
                        return (False, sorted_list.index(x))

            get_back = check() if len(sorted_list) != 0 else (0, 0)
            to_insert, idx = get_back[0], get_back[1]

            if len(sorted_list) == 0:
                sorted_list.append(member)

            elif to_insert:
                sorted_list.insert(idx, member)
            elif not to_insert:
                sorted_list.append(member)

        return sorted_list

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
            'name': author.nickname,
            'score': 0
        }
        self.update_data(data)

    def reg_guild(self, guild, author):
        data = self.get_data()
        guild_id = str(guild.id)
        data[guild_id] = {
            'excluded_channels': []
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

    def decode_mention(self, mention: str):
        mention = mention.replace('<', '')
        mention = mention.replace('@', '')
        mention = mention.replace('>', '')
        mention = mention.replace('!', '')
        return mention

    def decode_channel(self, channel: str):
        channel = channel.replace('<', '')
        channel = channel.replace('#', '')
        channel = channel.replace('>', '')
        channel = channel.replace('!', '')
        return channel

    def member_exists(self, mention, guild):
        mention = self.decode_mention(mention)
        try:
            int(mention)
        except:
            return False

        server = self.bot.get_guild(guild.id)
        if server.get_member(int(mention)) is None:
            return False

        else:
            member = server.get_member(int(mention))
            data = self.get_data()

            if str(member.id) not in data[str(guild.id)] and not member.bot:
                self.reg_member(guild, member)

        return True

    def make_three_digit(self, num:int):
        num = str(num)
        if len(num) == 1:
            num = f'00{num}'
        elif len(num) == 2:
            num = f'0{num}'
        
        return num

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_message(self, message):
        data = self.get_data()

        if message.author.bot:
            return
        if message.channel.id in data[str(message.guild.id)]['excluded_channels']:
            return

        self.check_guild(message.guild, message.author)

        data[str(message.guild.id)][str(message.author.id)]['name'] = message.author.nickname
        data[str(message.guild.id)][str(message.author.id)]['score'] += 1

        self.update_data(data)

    @commands.group(name='tier', invoke_without_command=True)
    @commands.guild_only()
    async def tier(self, ctx: Context):
        await ctx.send('Command cannot be invoked without a subcommand. Use `$help tier` for more info.')

    @tier.command()
    async def score(self, ctx: Context, member=None):
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
        embed.add_field(name='Messaging Score',
                        value=f'Your messaging score is `{data[str(ctx.guild.id)][str(member.id)]["score"]}`.')
        await ctx.reply(embed=embed, mention_author=False)

    @tier.command()
    @commands.has_permissions(administrator=True)
    async def exclude(self, ctx:Context, channel=None):
        self.check_guild(ctx.guild, ctx.author)
        if channel is None:
            await ctx.send(f'What channel would you like scores to be not counted from?')
            channel = await self.bot.wait_for('message')

        if '<#' in channel and '>' in channel:
            channel = ctx.guild.get_channel(int(self.decode_channel(channel)))
        else:
            await ctx.send('Channel not found.')
            return

        data = self.get_data()
        if channel.id in data[str(ctx.guild.id)]['excluded_channels']:
            await ctx.send(f'Channel {channel.mention} is already excluded from coutning scores.')
            return 
        
        data[str(ctx.guild.id)]['excluded_channels'].append(channel.id)
        self.update_data(data)

        await ctx.send(f'Messages in channel {channel.mention} will no longer add your score.')

    @exclude.error
    async def exclude_error(self, ctx:Context, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have the clearance level to use this command.')
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('Channel not found.')

    @tier.command()
    @commands.has_permissions(administrator=True)
    async def include(self, ctx, channel=None):
        self.check_guild(ctx.guild, ctx.author)
        if channel is None:
            await ctx.send(f'What channel would you like scores to be counted from?')
            channel = await self.bot.wait_for('message')

        if '<#' in channel and '>' in channel:
            channel = ctx.guild.get_channel(int(self.decode_channel(channel)))
        else:
            await ctx.send('Channel not found.')
            return

        data = self.get_data()
        if channel.id not in data[str(ctx.guild.id)]['excluded_channels']:
            await ctx.send(f'Channel {channel.mention} is already included from counting scores.')
            return 
        
        data[str(ctx.guild.id)]['excluded_channels'].remove(channel.id)
        self.update_data(data)

        await ctx.send(f'Messages in channel {channel.mention} will now add your score.')

    @include.error
    async def include_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have the clearance level to use this command.')
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('Channel not found.')

    @tier.command()
    async def excluded(self, ctx:Context):
        self.check_guild(ctx.guild, ctx.author)
        data = self.get_data()
        channels = data[str(ctx.guild.id)]['excluded_channels']
        embed = discord.Embed(title='Excluded Channels', description='List of channels excluded from increasing messaging scores.', color=PURPLE)
        if len(channels) > 0:
            excluded_channels = ''
            for channel in channels:
                channel = ctx.guild.get_channel(channel)
                excluded_channels += channel.mention + '\n'
            embed.add_field(name='List:', value=excluded_channels)
        else:
            embed.add_field(name='List:', value='No channels are excluded.')
        
        await ctx.reply(embed=embed, mention_author=False)
        return

    @tier.command(aliases=['lb'])
    async def leaderboard(self, ctx, page_number=1):
        self.check_guild(ctx.guild, ctx.author)
        data = self.get_data()[str(ctx.guild.id)]
        members = []
        for member in data:
            if member == 'excluded_channels':
                continue
            else:
                members.append((data[member]['name'], data[member]['score']))

        members = self.sort_members(members)
        members.reverse()

        embed = discord.Embed(title='**LEADERBOARD**', description='Leaderboard of messaging scores for this server.', color=PURPLE)
        pages = []
        rank = 1
        page = []
        for member in members:
            medal = ''

            if rank == 1:
                medal = '🥇'
            elif rank == 2:
                medal = '🥈'
            elif rank == 3:
                medal = '🥉'
            elif rank > 3 and rank < 11:
                medal = '🎖'

            page.append(f'{self.make_three_digit(rank)} ∙ {member[0]}{medal} [{member[1]}]')
            if len(page) == 10:
                pages.append(page)
                page=[]
            
            rank += 1
        
        if page not in pages:
            pages.append(page)
            page = []

        page_str = ''
        page_count = len(pages)
        for member in pages[page_number-1]:
            page_str += member + '\n'

        embed.add_field(name='Rank∙ Name [Score]', value='```'+page_str+'```')
        embed.set_footer(text=f'Showing page ({page_number}/{len(pages)}).\nUse {ctx.prefix}tier {ctx.invoked_with} <page number>.')

        await ctx.reply(embed=embed, mention_author=False)

    @leaderboard.error
    async def lb_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            embed = discord.Embed(title='Error 404', description='Page not found', color=PURPLE)
            await ctx.reply(embed=embed, mention_author=False)


def setup(bot):
    bot.add_cog(Cog(bot))
