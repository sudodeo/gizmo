import discord
from discord import app_commands
from discord.ext import commands
from apis.magiceden import Magiceden
from datetime import datetime
from typing import List
from discord.errors import HTTPException


class MagicedenCog(commands.Cog, name="Magiceden"):
    def __init__(self, bot):
        self.bot = bot

    async def collection_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> List[app_commands.Choice[str]]:

        if current != []:
            db = self.bot.conn
            # % is a wildcard
            symbols = await db.fetch(f"""SELECT * FROM magiceden 
                                        WHERE LOWER(name) LIKE '%{current.lower()}%' 
                                        ORDER BY CASE WHEN LOWER(name) LIKE '{current.lower()}' THEN 0 
                                                    WHEN LOWER(name) LIKE '{current.lower()}%' THEN 1
                                                    WHEN LOWER(name) LIKE '%{current.lower()}' THEN 3
                                                        ELSE 2
                                                        END""")
            if symbols:
                return [app_commands.Choice(value=symbol['symbol'], name=symbol['name']) for symbol in symbols][:25]

    @commands.hybrid_command()
    @app_commands.autocomplete(collection=collection_autocomplete)
    async def me(self, ctx: commands.Context, *, collection: str):
        """Get collection details from Magiceden marketplace"""
        async with ctx.typing():
            magiceden = Magiceden()
            collection_details = await magiceden.get_collection_details(collection)
            time = datetime.now()

            if type(collection_details) == dict:

                name, image, collection_magiceden_url, logo, website, twitter, discord_server, stats = collection_details.values()

                embed = discord.Embed(title=name, url=collection_magiceden_url,
                                      color=discord.Colour.green(), timestamp=time)

                embed.add_field(name="Floor Price",
                                value=stats.get("floor price") or "None")
                # embed.add_field(name="Total Supply", value=stats.get("total supply"), inline=False)
                embed.add_field(name="Total Volume",
                                value=stats.get("total volume") or "None")
                embed.add_field(name="Avg Price 24hr",
                                value=stats.get("avg price 24hr") or "None")
                embed.add_field(name="Listed NFTs", value=stats.get(
                    "listed count") or "None")
                if website not in [None, ""]:
                    embed.add_field(
                        name="Website", value=f"[Visit]({website})")
                if twitter not in [None, ""]:
                    embed.add_field(
                        name="Twitter", value=f"[@{twitter}]")
                if discord_server not in [None, ""]:
                    embed.add_field(
                        name="Discord Server", value=f"[Join]({discord_server})")
                embed.set_thumbnail(url=image)

                embed.set_footer(
                    text="Built by grim.reaper#9626", icon_url=logo)

                await ctx.reply(embed=embed)

            else:
                # print(collection)

                embed = discord.Embed(
                    title="Collection not found", color=discord.Colour.red(), timestamp=time)
                # embed.set_thumbnail(url=collection_details[1])
                embed.add_field(
                    name="Try", value="Checking collection on coralcube")
                embed.set_image(
                    url="https://c.tenor.com/8RRUPtXrEcgAAAAS/osita-osita-iheme.gif")
                embed.set_footer(text="Built by grim.reaper#9626",
                                 icon_url=collection_details[1])

                await ctx.reply(embed=embed)

    @me.error
    async def on_me_error(self, ctx: commands.Context, error):
        error = getattr(error, 'original', error)
        if isinstance(error, HTTPException):
            pass
        owner = self.bot.get_user(741308876204408854)
        await ctx.reply("An error occured. Contact grim.reaper#9626 for support", delete_after=5)
        await owner.send(f"{error}\n{ctx.kwargs}")


async def setup(bot):
    await bot.add_cog(MagicedenCog(bot))
