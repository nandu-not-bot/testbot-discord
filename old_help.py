import discord
from discord.ext import commands
from discord.ext.commands.context import Context

PURPLE = 0x510490


class CommandGroup:
    def __init__(self, title, command, commands={}) -> None:
        self.title = title
        self.command = command
        self.commands = commands


class Command:
    def __init__(self, command, discription, usage, output=None, aliases=None):
        self.command = command
        self.discription = discription
        self.usage = usage
        self.output = output
        self.aliases = aliases


class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx: Context, group=None, subcommand=None):
        groups = {
            "math": CommandGroup(
                "**🤓 Math**",
                f"`{ctx.prefix}help math`",
                {
                    "add": Command(
                        "Add",
                        "Adds given numbers and returns the sum.",
                        f"`{ctx.prefix}add <[a b c ...]>`",
                        output="`a + b + c + ... = (sum)`",
                    ),
                    "sub": Command(
                        "Subtract",
                        "Subtracts two given numbers and returns the difference.",
                        f"`{ctx.prefix}sub <x> <y>`",
                        output="`x - y = (difference)`",
                    ),
                    "mult": Command(
                        "Multiply",
                        "Mulitplies given numbers and returns the product.",
                        f"`{ctx.prefix}mult <[a b c ...]>`",
                        output="`a * b * c * ... = (product)`",
                    ),
                    "div": Command(
                        "Divide",
                        "Divides two given numbers and returns the quotient.",
                        f"`{ctx.prefix}div <x> <y>`",
                        output="`x / y = (quotient)`",
                    ),
                    "mean": Command(
                        "Mean",
                        "Gives the arithmetic mean or average of a list of given numbers.",
                        f"`{ctx.prefix}mean <[a b c ...]>`",
                        output="`The arithmetical mean of [a b c ...] is (mean)`",
                    ),
                    "median": Command(
                        "Median",
                        "Gives the median of a list of given numbers.",
                        f"`{ctx.prefix}median <[a b c ...]>`",
                        output="`The median of [a b c ...] is (median)`",
                    ),
                    "mode": Command(
                        "Mode",
                        "Gives the arithemetic mode of given list of numbers.",
                        f"`{ctx.prefix}mode <[a b c ...]>`",
                        output="`The mode of [a b c ...] is (mode) occuring at a total of (count) times.`",
                    ),
                },
            ),
            "cc": CommandGroup(
                "**🤖 Custom Commands**",
                f"`{ctx.prefix}help cc`",
                {
                    "list": Command(
                        "List",
                        "Shows a list of all the custom commands and replies on this server.",
                        f"`{ctx.prefix}cc list`",
                    ),
                    "add": Command(
                        "Add",
                        "Add a reply to an existing custom command or create a new custom command.",
                        f"`{ctx.prefix}cc add |custom command|`",
                    ),
                    "toggle": Command(
                        "Toggle custom command",
                        "Toggles a custom command on or off for the server.",
                        f"`{ctx.prefix}cc toggle |custom command|`",
                    ),
                    "enable": Command(
                        "Enable cc",
                        "Enables all custom commands for this server.",
                        f"`{ctx.prefix}cc enable`",
                    ),
                    "disable": Command(
                        "Disable cc",
                        "Disables all custom commands for this server.",
                        f"`{ctx.prefix}cc enable`",
                    ),
                    "remove": Command(
                        "Remove Reply",
                        "Removes specific replies from custom commands.",
                        f"`{ctx.prefix}cc remove |custom command|`",
                    ),
                },
            ),
            "fun": CommandGroup(
                "**🎮 Fun**",
                f"`{ctx.prefix}help fun`",
                {
                    "xo": Command(
                        "TicTacToe",
                        "Play TicTacToe with another player!",
                        f"`{ctx.prefix}xo <@player 2>`",
                        aliases=["`ttt`", "`tictactoe`"],
                        name="xo",
                    ),
                    "rps": Command(
                        "Rock Paper Scissors",
                        "I play a game of rock paper scissors with you!",
                        f"`{ctx.prefix}rps`",
                        name="rps",
                    ),
                    "ask": Command(
                        "Ask Question",
                        "Ask a question and get an answer as a quote. from a very famous person. (8ball but better)",
                        f"`{ctx.prefix}ask <question>`",
                        name="ask",
                    ),
                },
            ),
            "misc": CommandGroup(
                "**✨ Misc**",
                f"`{ctx.prefix}help misc`",
                {
                    "coolbot": Command(
                        "Cool Bot 😎",
                        "Find out for yourself. ;)",
                        f"`{ctx.prefix}coolbot`",
                        name="coolbot",
                    )
                },
            ),
            "ms": CommandGroup(
                "**🎖 Messaging Scores**",
                f"`{ctx.prefix}help ms`",
                {
                    "deduct": Command(
                        "Deduct Point",
                        "Deducts messaging points from a user. (Admins Only)",
                        f"`{ctx.prefix}tier deduct |mention member|`",
                        "deduct",
                    ),
                    "score": Command(
                        "Messaging Score",
                        "Shows score and rank of a person or yourself in this server.",
                        f"`{ctx.prefix}tier score |mention member|`",
                        "score",
                    ),
                    "exclude": Command(
                        "Exclude Channel",
                        "Excludes said channel from adding up your scores. Useful to nerf spam channels etc.",
                        f"`{ctx.prefix}tier exclude |#channel|`",
                        "exclude",
                    ),
                    "excluded": Command(
                        "Excluded Channels List",
                        "Shows list of all the channels excluded from adding scores.",
                        f"`{ctx.prefix}tier excluded`",
                        "excluded",
                        aliases=["`list`", "`leaderboard`"],
                    ),
                    "include": Command(
                        "Include Channel",
                        "Includes said channel to add scores.",
                        f"`{ctx.prefix}tier include |#channel|`",
                        "include",
                    ),
                    "leaderboard": Command(
                        "Leaderboard",
                        "Shows the leaderboard of messaging scores for this server",
                        f"`{ctx.prefix}ms leaderboard`",
                        "leaderboard",
                        aliases=["`lb`", "`leaderboard`"],
                    )
                }
            )
        }

        all_command_names = []
        # for g in groups:
        #     for c in g.commands:
        #         all_command_names.append(c.name)

        if group not in groups:
            help = discord.Embed(
                title="Chitti Robo commands list",
                description="Help command for this bot.",
                color=PURPLE,
            )
            for group in groups:
                group = groups[group]
                help.add_field(name=group.title, value=group.command, inline=True)
            help.set_footer(text="Dm nandu<3#8677 for suggestions on this bot. :)")
            await ctx.reply(embed=help, mention_author=False)

        elif group in groups and subcommand is None:
            help = discord.Embed(
                title=f"{group.capitalize()} commands",
                description=f"List of {group} commands for this bot.",
                color=PURPLE,
            )
            group = groups[group]
            for c in group.commands:
                help.add_field(name=c.command, value=c.usage, inline=True)
            help.set_footer(
                text=f"Use `{ctx.prefix}help {group.name} <command>` for more info on each command.\nSyntax: <required> [infinite list of numbers...] |optional|"
            )
            await ctx.reply(embed=help, mention_author=False)

        elif group in group_names and subcommand in all_command_names:
            command = None
            for g in groups:
                for c in g.commands:
                    if c.name == subcommand and group == g.name:
                        command = c

            if command is None:
                await ctx.reply(
                    f'Subcommand "{subcommand}" not found in group "{group}".'
                )
                return

            help = discord.Embed(
                title=command.command, color=PURPLE, description=command.discription
            )
            help.add_field(name="Usage", value=command.usage)
            if command.aliases != None:
                aliases = "".join(a + "   " for a in command.aliases)
                help.add_field(name="Aliases", value=aliases)
            if command.output != None:
                help.add_field(name="Output", value=command.output)

            help.set_footer(
                text="Syntax: <required> [infinite list of numbers...] |optional|"
            )
            await ctx.reply(embed=help)


def setup(bot):
    bot.add_cog(Cog(bot))
