from discord.ext import commands


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="ping")
    async def ping(self, ctx: commands.Context) -> None:
        """ Check if bot is online """
        await ctx.reply(f"Pong!\nBot Speed: {(self.bot.latency * 1000):.2f}ms")
    # @commands.command()
    # async def welcome(self, ctx, ):

    #     await ctx.send(f'Welcome to my turf bozo <@772786473912631316>')

    @commands.hybrid_command()
    async def cleanup(self, ctx: commands.Context, amount: int) -> None:
        """ Purge messages """
        if ctx.author.resolved_permissions.manage_messages:
            await ctx.channel.purge(limit=amount)
            await ctx.send(f'{amount} messages deleted', delete_after=5.0, ephemeral=True)
        else:
            await ctx.send('You do not have the required permissions to use this command', ephemeral=True, delete_after=5.0)

    @cleanup.error
    async def cleanup_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        """ Purge error """
        await ctx.send(f'Error: {error}')

    # def is_in_guild(guild_id):
    #     async def predicate(ctx):
    #         return ctx.guild and ctx.guild.id == guild_id
    #     return commands.check(predicate)

    # @commands.hybrid_command()
    # @commands.is_owner()
    # @is_in_guild(935741302769844244)
    # async def sync():
    #     pass

async def setup(bot):
    await bot.add_cog(Test(bot))
