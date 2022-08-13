from typing import List
from unicodedata import name
import discord
from discord import app_commands
from discord.ext import commands
from apis.opensea import Opensea
from datetime import datetime


class OpenseaCog(commands.Cog, name="Opensea"):
    def __init__(self, bot):
        self.bot = bot

    async def collection_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> List[app_commands.Choice[str]]:

        db = self.bot.conn
        # % is a wildcard
        symbols = await db.fetch(f"""SELECT * FROM opensea 
                                    WHERE LOWER(name) LIKE '%{current.lower()}%' 
                                    ORDER BY CASE WHEN LOWER(name) LIKE '{current.lower()}' THEN 0 
                                                WHEN LOWER(name) LIKE '{current.lower()}%' THEN 1
                                                WHEN LOWER(name) LIKE '%{current.lower()}' THEN 3
                                                    ELSE 2
                                                    END, name ASC LIMIT 30""")

        return [app_commands.Choice(value=symbol['symbol'], name=symbol['name']) for symbol in symbols if symbol['name'] != ""][:25]

    @commands.hybrid_command()
    @app_commands.autocomplete(collection=collection_autocomplete)
    async def os(self, ctx: commands.Context, *, collection: str):
        """Get collection details from Opensea marketplace"""
        async with ctx.typing():
            collection_details = await Opensea().get_collection_details(collection)
            time = datetime.now()

            if type(collection_details) == dict:
                name, logo, image, opensea_url, website, twitter, discord_server, stats = collection_details.values()

                embed = discord.Embed(
                    title=name, url=opensea_url, color=discord.Colour.green(), timestamp=time)
                # embed.add_field(name="Name", value=name, inline=False)
                embed.add_field(name="Floor Price",
                                value=stats.get("floor price"))
                embed.add_field(name="Total Supply", value=int(
                    stats.get("total supply")))
                embed.add_field(name="Total Volume",
                                value=stats.get("total volume"))
                embed.add_field(name="Avg Price 24hr",
                                value=stats.get("avg price 24hr"))
                embed.add_field(name="Unique Holders",
                                value=stats.get("unique holders"))
                embed.add_field(
                    name="Website", value=f"[Visit]({website})")
                embed.add_field(name="Twitter", value=f"[View]({twitter})")
                embed.add_field(
                    name="Discord", value=f"[Join]({discord_server})")
                embed.set_thumbnail(url=image)
                embed.set_footer(
                    text="Built by grim.reaper#9626", icon_url=logo)

                await ctx.reply(embed=embed)

            else:
                embed = discord.Embed(
                    title="Collection not found", color=discord.Colour.red(), timestamp=time)
                # embed.set_thumbnail(url=collection_details[1])
                embed.add_field(
                    name="Try", value="Check spelling", inline=False)
                embed.add_field(
                    name="Try", value="compound name collections should look like:\nboredapeyachtclub or mutant-ape-yacht-club", inline=False)
                embed.set_image(
                    url="https://c.tenor.com/8RRUPtXrEcgAAAAS/osita-osita-iheme.gif")
                embed.set_footer(text="Built by grim.reaper#9626",
                                 icon_url=collection_details[1])
                await ctx.reply(embed=embed)

    @os.error
    async def on_os_error(self, ctx: commands.Context, error):
        error = getattr(error, 'original', error)
        owner = self.bot.get_user(741308876204408854)
        await ctx.reply("An error occured. Contact grim.reaper#9626 for support", delete_after=5)
        await owner.send(f"{error}\n{ctx.kwargs}")


async def setup(bot):
    await bot.add_cog(OpenseaCog(bot))
