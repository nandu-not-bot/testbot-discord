from dataclasses import asdict
from re import L

import discord
from discord.ext.commands import context
from replit import db
from discord.ext import commands
from discord.ext.commands.context import Context

from classes import Guild, Member
from embeds import MessagingScoreEmbeds, GeneralEmbeds


class Cog(commands.Cog):

    """Messaging scores"""

    def __init__(self, bot):
        self.bot = bot

    # METHODS

    # Decode mention
    @staticmethod
    def decode_mention(mention: str) -> int:
        mention = mention.replace("<", "")
        mention = mention.replace("@", "")
        mention = mention.replace("#", "")
        mention = mention.replace(">", "")
        mention = mention.replace("!", "")
        return mention

    # Get guild and member
    @staticmethod
    def get_guild(id: int) -> Guild:
        if str(id) in db:
            return Guild(**db[str(id)])
        else:
            return Guild(id)

    def get_member(self, guild: Guild, id: int, display_name: str) -> Member:
        for member in guild.members:
            if member["id"] == id:
                member = Member(**member)
                member.display_name = display_name
                return member

        self.dump(guild, member)
        return Member(id, display_name)

    # Dump guild and member
    @staticmethod
    def dump(guild: Guild, member: Member = None):
        if member is not None:
            guild.members[str(member.id)] = asdict(member)

        db[str(guild.id)] = asdict(guild)

    # Get member from mention
    def find_member(self, ctx: Context, mention: str):
        member_id = self.decode_mention(mention)
        try:
            member_id = int(member_id)
        except:
            return

        guild = self.get_guild(ctx.guild.id)
        if (
            ctx.guild.get_member(member_id) is None
            or ctx.guild.get_member(member_id).bot
        ):
            return
        else:
            return self.get_member(guild, member_id, ctx.author.display_name)

    # COMMANDS

    # On message
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Updates Scores on message"""

        if message.author.bot:
            return

        guild = self.get_guild(message.guild.id)
        member = self.get_member(guild, message.author.id, message.author.display_name)

        if message.channel.id in guild.excluded_channels:
            return

        member.score += 1

        self.dump(guild, member)

    # Parent
    @commands.group(aliases=["tier"], invoke_without_command=True)
    async def ms(self, ctx: Context):
        """Parent Command For Messaging Scores Subcommands"""

        await ctx.reply(
            "Uh oh! Cannot use command without a valid subcommand!",
            mention_author=False,
        )

    # Score
    @ms.command()
    async def score(self, ctx: Context, mention: str = None):
        """Shows score of user if mentioned else shows score of invoker."""

        if mention is None or self.find_member(ctx, mention) is None:
            member = self.get_member(ctx.author.id)
        else:
            member = self.find_member(ctx, mention)

        pfp_url = member.get_avatar_url(self.bot, self.get_guild(ctx.guild.id))

        await ctx.send(
            embed=MessagingScoreEmbeds.Score.show_score(
                member.display_name,
                pfp_url,
                member.score,
                self.get_guild(ctx.guild.id).get_leaderboard().index(member) + 1,
            )
        )

    # Leaderboard
    @ms.command(aliases=["leaderboard", "board"])
    async def lb(self, ctx: Context, page: int):
        """Shows messaging score leaderboard for the server"""

    # Exclude
    @ms.command()
    async def exclude(self, ctx: Context, mention):
        """Excludes a channel from adding up messaginf scores."""

    # Include
    @ms.command()
    async def include(self, ctx: Context, mention):
        """Includes a channel for adding up messaging scores."""

    # Excluded
    @ms.command(alisases=["list"])
    async def excluded(self, ctx: Context):
        """Shows channels excluded from messaging scores."""

    # Deduct
    @ms.command()
    async def deduct(self, ctx: Context, mention):
        """Deducts points from a member."""


def setup(bot):
    bot.add_cog(Cog(bot))
