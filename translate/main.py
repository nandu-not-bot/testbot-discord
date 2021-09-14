from logging import lastResort
import discord
from discord.ext import commands
from discord.ext.commands.context import Context
from googletrans import Translator, LANGUAGES


class Cog(commands.Cog):

    """Translate Cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['detect', 'lang'])
    async def detectlang(self, ctx: Context, text: str = None):

        """$detectlang <text>"""

        if text is None:
            await ctx.send(
                embed=discord.Embed(
                    description="Wha...? What should i detect?", color=0xFF0000
                )
            )
            return

        translator = Translator()

        result = translator.detect(text)

        lang, certainity = LANGUAGES[result.lang].title(), result.confidence * 100

        await ctx.send(
            embed=discord.Embed(
                title=f"{lang}!",
                description=f"I'm `{int(certainity)}%` sure that `{text}` is in {lang}.",
                color=0xFF0000,
            )
        )

    @commands.command(aliases=['langs'])
    async def langlist(self, ctx: Context):

        """$langlist"""

        langs = [f"`{lang} - {LANGUAGES[lang]}`, " for lang in LANGUAGES]

        await ctx.send(
            embed=discord.Embed(title="Language Codes", description="".join(*langs)[-2])
        )

    @commands.command()
    async def translate(self, ctx: Context, *args):

        '''$translate <text> [?language code]'''

        if args[-1][0] != '?':
            langcode = 'en'
            text_ = ''.join(args)
        else:
            langcode = args[-1][1:].lower()
            text_ = ''.join(args[:-1])

        if text_ < 0 or langcode not in LANGUAGES:
            await ctx.send(f"❌ Please enter a valid language code and use '?'.\n***Eg:** `{ctx.prefix}translate Random text ?ja`")
            return

        translator = Translator()
        result = translator.translate(text_, dest=langcode)

        translation, src, dest, pronounciation = result.text, result.src, result.dest, result.pronunciation

        embed = discord.Embed(
            title = "FOUND IT!",
            color = 0x00ff00
        )
        embed.add_field(
            name="Original text",
            value=f"`{text_}`"
        )
        embed.add_field(
            name="Original language",
            value=f"`{LANGUAGES[src].title()}`"
        )
        embed.add_field(
            name="Translated to",
            value=f"`{LANGUAGES[dest].title()}`"
        )
        embed.add_field(
            name="Translation",
            value=f"`{translation}`"
        )
        embed.add_field(
            name="Pronounciation",
            value=f"`{pronounciation}`"
        )

        await ctx.send()

def setup(bot):
    bot.add_cog(Cog(bot))
