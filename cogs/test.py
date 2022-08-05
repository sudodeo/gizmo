from discord.ext import commands
from discord import app_commands
import discord

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.command()
    # async def test(self, ctx):
    #     await ctx.message.reply('lfg')

    @commands.hybrid_command(name="ping")
    async def ping(self, ctx: commands.Context) -> None:
        """ /command-1 """
        await ctx.send("Pong!")
    # @commands.command()
    # async def welcome(self, ctx, ):
        
    #     await ctx.send(f'Welcome to my turf bozo <@772786473912631316>')

async def setup(bot):
    await bot.add_cog(Test(bot))