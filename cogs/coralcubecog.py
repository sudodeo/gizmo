from typing import List
import discord
from discord import app_commands
from discord.ext import commands
from apis.coralcube import Coralcube
from datetime import datetime


class CoralcubeCog(commands.Cog, name="Coralcube"):
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
    async def cc(self, ctx, *, collection: str):
        """Get collection details from Coralcube marketplace"""
        async with ctx.typing():
            coralcube = Coralcube()
            collection_details = await coralcube.main(collection)
            time = datetime.now()

            if type(collection_details) == dict:

                name, image, collection_coralcube_url, logo, website, twitter, discord_server, stats = collection_details.values()

                embed = discord.Embed(title=name, url=collection_coralcube_url,
                                      color=discord.Colour.green(), timestamp=time)

                embed.add_field(name="Floor Price",
                                value=stats.get("floor price") or "None")
                embed.add_field(name="Total Supply",
                                value=stats.get("total supply"))
                embed.add_field(name="7-day Volume",
                                value=stats.get("seven day volume") or "None")
                # embed.add_field(name="Avg Price 24hr", value=stats.get("avg price 24hr") or "None", inline=False)
                embed.add_field(name="Listed NFTs", value=stats.get(
                    "listed count") or "None")
                embed.add_field(name="Unique Holders",
                                value=stats.get("unique holders") or "None")
                if website not in [None, ""]:
                    embed.add_field(
                        name="Website", value=f"[Visit]({website})")
                if twitter not in [None, ""]:
                    embed.add_field(
                        name="Twitter", value=f"[@{twitter.split('/')[-1]}]({twitter})")
                if discord_server not in [None, ""]:
                    embed.add_field(
                        name="Discord Server", value=f"[Join]({discord_server})")
                embed.set_thumbnail(url=image)

                embed.set_footer(
                    text="Built by grim.reaper#9626", icon_url=logo)

                await ctx.reply(embed=embed)

            else:

                embed = discord.Embed(
                    title="Collection not found", color=discord.Colour.red(), timestamp=time)
                # embed.set_thumbnail(url=collection_details[1])
                embed.add_field(
                    name="Try", value="Checking collection on magiceden")
                embed.set_image(
                    url="https://c.tenor.com/8RRUPtXrEcgAAAAS/osita-osita-iheme.gif")
                embed.set_footer(text="Built by grim.reaper#9626",
                                 icon_url=collection_details[1])

                await ctx.reply(embed=embed)

    @cc.error
    async def on_cc_error(self, ctx, error):
        error = getattr(error, 'original', error)
        owner = self.bot.get_user(741308876204408854)
        await ctx.reply("An error occured. Contact grim.reaper#9626 for support", delete_after=5)
        await owner.send(f"{error}\n{ctx.kwargs}")


async def setup(bot):
    await bot.add_cog(CoralcubeCog(bot))
