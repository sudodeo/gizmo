import discord
from discord import app_commands
from discord.ext import commands
from dictionary import AntiBozo



class Dictionary(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dictionary = AntiBozo()

    @app_commands.command()
    async def search(self, interaction: discord.Interaction, word: str):
        """Search word in dictionary"""
        
        # await ctx.send(word)
        definition, part_of_speech = self.dictionary.word_search(word)
        print(definition)
        if definition:
            embed = discord.Embed(title=f"{word}", description=f"{definition}", color=0x00ff00)
        
            embed.set_footer(text=f"{part_of_speech}")

            await interaction.response.send_message(embed=embed)
        else:
            print("No definition found")
            embed = discord.Embed(title="No definition found")
            await interaction.response.send_message(embed=embed)

    @app_commands.command()
    async def word_of_the_day(self, interaction: discord.Interaction):
        """Returns word of the day"""
        word, part_of_speech, definition, examples, note = self.dictionary.word_of_the_day().values()
        print(word)
        embed = discord.Embed(title=word, description=definition, colour=discord.Colour.random())
        embed.add_field(name="Part of speech", value=part_of_speech, inline=False)
        embed.add_field(name="Example", value=examples, inline=False)
        embed.add_field(name="Note", value=note, inline="False")

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Dictionary(bot))
