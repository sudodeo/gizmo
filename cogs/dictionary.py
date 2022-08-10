import discord
from discord import app_commands
from discord.ext import commands
from apis.dictionary import AntiBozo
from datetime import datetime


class Dictionary(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dictionary = AntiBozo()

    @app_commands.command()
    async def search(self, interaction: discord.Interaction, word: str):
        """Search word in dictionary"""
        time = datetime.now()
        definition, part_of_speech = await self.dictionary.word_search(word)
        # print(definition)
        if definition:
            embed = discord.Embed(
                title=f"{word}", description=f"{definition}", color=discord.Colour.green(), timestamp=time)

            embed.set_footer(text=f"{part_of_speech}")

            await interaction.response.send_message(embed=embed)
        else:
            print("No definition found")
            embed = discord.Embed(
                title="No definition found", colour=discord.Colour.red(), timestamp=time)
            await interaction.response.send_message(embed=embed)

    @app_commands.command()
    async def word_of_the_day(self, interaction: discord.Interaction):
        """Returns word of the day"""
        time = datetime.now()
        word, part_of_speech, definition, examples, note = await self.dictionary.word_of_the_day().values()
        # print(word)
        embed = discord.Embed(title=word, description=definition,
                              colour=discord.Colour.random(), timestamp=time)
        embed.add_field(name="Part of speech",
                        value=part_of_speech, inline=False)
        embed.add_field(name="Example", value=examples, inline=False)
        embed.add_field(name="Note", value=note, inline="False")

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Dictionary(bot))
