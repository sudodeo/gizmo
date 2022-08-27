from typing import List
import discord
from discord import app_commands
from discord.ext import commands
from apis.coralcube import Coralcube
from datetime import datetime


class SellWall(commands.Cog, name="Sell Wall"):
    def __init__(self, bot):
        self.bot = bot

    async def collection_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> List[app_commands.Choice[str]]:
        db = self.bot.conn
        # % is a wildcard
        symbols = await db.fetch(f"""SELECT * FROM coralcube 
                                    WHERE LOWER(name) LIKE '%{current.lower()}%' 
                                    ORDER BY CASE WHEN LOWER(name) LIKE '{current.lower()}' THEN 0 
                                                WHEN LOWER(name) LIKE '{current.lower()}%' THEN 1
                                                WHEN LOWER(name) LIKE '%{current.lower()}' THEN 3
                                                    ELSE 2
                                                    END, name ASC LIMIT 30""")

        return [app_commands.Choice(value=symbol['symbol'], name=symbol['name']) for symbol in symbols if symbol['name'] != ""][:25]

    @commands.hybrid_command()
    @app_commands.autocomplete(collection=collection_autocomplete)
    async def sell_wall(self, ctx, *, collection: str, price: int):
        """Check sell wall for an NFT collection"""
        async with ctx.typing():
            coralcube = Coralcube()
            collection_details = await coralcube.sell_wall(collection, price)
            time = datetime.now()

            if type(collection_details) == list:

                total_listings, listed_count, percentage, floor_price, collection_image, collection_name, collection_url = collection_details

                embed = discord.Embed(title=collection_name, url=collection_url,
                                      color=discord.Colour.green(), timestamp=time)

                embed.add_field(
                    name="Sell Wall", value=f"There are {listed_count} NFTs listed under {price} ◎ \n({percentage}%)")

                embed.add_field(name="Floor Price",
                                value=f"{floor_price} ◎", inline=False)

                embed.add_field(name="Total Listings",
                                value=f"{total_listings}")

                embed.set_thumbnail(url=collection_image)

                embed.set_footer(text="Built by grim.reaper#9626")

                await ctx.reply(embed=embed)

            else:

                embed = discord.Embed(
                    title="Collection not found", color=discord.Colour.red(), timestamp=time)
                embed.set_image(
                    url="https://c.tenor.com/8RRUPtXrEcgAAAAS/osita-osita-iheme.gif")
                embed.set_footer(text="Built by grim.reaper#9626")

                await ctx.reply(embed=embed)

    @sell_wall.error
    async def on_sell_wall_error(self, ctx, error):
        error = getattr(error, 'original', error)
        owner = self.bot.get_user(741308876204408854)
        await ctx.reply("An error occured. Contact grim.reaper#9626 for support", delete_after=5)
        await owner.send(f"{error}\n{ctx.kwargs}")


async def setup(bot):
    await bot.add_cog(SellWall(bot))
