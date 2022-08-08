from discord.ext import commands



class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="ping")
    async def ping(self, ctx: commands.Context) -> None:
        """ Check if bot is online """
        await ctx.reply(f"Pong!->\nBot Speed: {(self.bot.latency * 1000):.2f}ms")
    # @commands.command()
    # async def welcome(self, ctx, ):

    #     await ctx.send(f'Welcome to my turf bozo <@772786473912631316>')


async def setup(bot):
    await bot.add_cog(Test(bot))
