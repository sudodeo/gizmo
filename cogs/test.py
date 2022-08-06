from discord.ext import commands
from discord import app_commands
import discord


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.command()
    # async def add_emoji(self, ctx):
    #     emoji_commands = ["e!add 7390-pepe-think", "e!add 7772-pepe-boxer", "e!add 5413-pepesadcry", "e!add 9605-pepe-business", "e!add 9347-pepe-shutup", "e!add 2763-suske", "e!add 2682-peepom16",
    #                       "e!add 8709-peepoexit", "e!add 7739-monkathink", "e!add 9529-pepe", "e!add 5600-pepepray", "e!add 6774-clownmirror", "e!add 9788-pepefuck", "e!add 5443-peepobusinesstux", "e!add 7245-pepe-out"]
    #     for e in emoji_commands:
    #         await ctx.send(e)

    @commands.hybrid_command(name="ping")
    async def ping(self, ctx: commands.Context) -> None:
        """ Check if bot is online """
        await ctx.send("Pong!")
    # @commands.command()
    # async def welcome(self, ctx, ):

    #     await ctx.send(f'Welcome to my turf bozo <@772786473912631316>')


async def setup(bot):
    await bot.add_cog(Test(bot))
