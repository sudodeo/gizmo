import discord
from discord import app_commands
from discord.ext import commands
from apis.coralcube import Coralcube
from datetime import datetime


class CoralcubeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    async def cc(self, interaction: discord.Interaction, collection: str):
        """Get collection details from Coralcube marketplace"""
        coralcube = Coralcube()
        collection_details = coralcube.get_collection_details(collection)
        time = datetime.now()

        if type(collection_details) == dict:

            name, image, collection_coralcube_url, logo, website, twitter, discord_server, stats = collection_details.values()

            embed = discord.Embed(title=name, url=collection_coralcube_url,
                                  color=discord.Colour.green(), timestamp=time)

            embed.add_field(name="Floor Price",
                            value=stats.get("floor price") or "None")
            embed.add_field(name="Total Supply",
                            value=stats.get("total supply"))
            embed.add_field(name="Total Volume",
                            value=stats.get("total volume") or "None")
            # embed.add_field(name="Avg Price 24hr", value=stats.get("avg price 24hr") or "None", inline=False)
            embed.add_field(name="Listed NFTs", value=stats.get(
                "listed count") or "None")
            embed.add_field(name="Unique Holders",
                            value=stats.get("unique holders") or "None")
            embed.add_field(
                name="Website", value=f"[Visit]({website})" or "None", inline=False)
            embed.add_field(
                name="Twitter", value=f"[View]({twitter})" or "None")
            embed.add_field(
                name="Discord", value=f"[Join]({discord_server})" or "None")
            embed.set_thumbnail(url=image)

            embed.set_footer(text="Built by grim.reaper#9626", icon_url=logo)

            await interaction.response.send_message(embed=embed)

        else:

            embed = discord.Embed(
                title="Collection not found", color=discord.Colour.red(), timestamp=time)
            embed.set_thumbnail(url=collection_details[1])
            embed.set_image(
                url="https://c.tenor.com/8RRUPtXrEcgAAAAS/osita-osita-iheme.gif")
            embed.set_footer(text="Built by grim.reaper#9626",
                             icon_url=collection_details[1])

            await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(CoralcubeCog(bot))
