from dataclasses import asdict

import discord
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

    # Make rank into a 000 format
    @staticmethod
    def format_rank(rank: int) -> str:
        rank = str(rank)
        if len(rank) == 1:
            return f"00{rank}"
        elif len(rank) == 2:
            return f"0{rank}"
        else:
            return rank

    # Add in k and M and all that to the score
    def add_suffix(score: int) -> str:
        if score >= 1000 and score < 10000:
            return f"{str(round(score/100, 1))}k"
        elif score >= 10000 and score < 1000000:
            return f"{str(score//100)}k"
        elif score >= 1000000:
            return f"{str(round(score/100000, 1))}M"

    # Make score look nice lol
    @staticmethod
    def format_score(score: int) -> str:
        score = str(score)
        return f'{score}{" "*(7-len(score))}'

    # Get medal
    @staticmethod
    def get_medal(rank: int):
        if rank == 1:
            return "🥇"
        elif rank == 2:
            return "🥈"
        elif rank == 3:
            return "🥉"

        return ""

    # Get guild and member
    @staticmethod
    def get_guild(id: int) -> Guild:
        if str(id) in db:
            return Guild(**db[str(id)])
        else:
            return Guild(id)

    def get_member(self, guild: Guild, id: int, display_name: str) -> Member:
        for member in guild.members:
            if guild.members[member]["id"] == id:
                member = Member(**guild.members[member])
                member.display_name = display_name
                return member

        self.dump(guild, Member(id, display_name))
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
            member = self.get_member(
                self.get_guild(ctx.guild.id), ctx.author.id, ctx.author.display_name
            )
        else:
            member = self.find_member(ctx, mention)

        pfp_url = member.get_avatar_url(self.bot, self.get_guild(ctx.guild.id))

        await ctx.reply(
            embed=MessagingScoreEmbeds.Score.show_score(
                member.display_name,
                pfp_url,
                member.score,
                member.get_rank(self.get_guild(ctx.guild.id)),
            ),
            mention_author=False,
        )

    # Leaderboard
    @ms.command(aliases=["leaderboard", "board"])
    async def lb(self, ctx: Context, page_no: int = None):
        """Shows messaging score leaderboard for the server"""

        if page_no is None:
            page_no = 1

        guild = self.get_guild(ctx.guild.id)
        leaderboard, pages = guild.get_leaderboard(page_no)
        page = [
            f'{self.format_rank(Member(**member).get_rank(guild))} ⫶ {self.format_score(self.add_suffix(member["score"]))} ⫶ {member["display_name"]} {self.get_medal(Member(**member).get_rank(guild))}'
            for member in leaderboard
        ]

        if not page:
            await ctx.reply(embed=MessagingScoreEmbeds.Lb.page_not_found())
            return

        embed = discord.Embed(
            title=f"Leaderboard of {ctx.guild.name}",
            description="Messaging scores leaderboard for this server.",
        )
        embed.add_field(
            name=f"RANK ⫶ SCORE ⫶ NAME",
            value="".join("`" + member + "`\n" for member in leaderboard),
        )
        embed.set_footer(
            text=f"Currently showing page ({page}/{pages}) \n Use {ctx.prefix}ms {ctx.command} <page no.> to show a specific page."
        )

        await ctx.reply(embed=embed)
        return

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
