import discord
from discord import app_commands
from discord.ext import commands
from apis.magiceden import Magiceden
from datetime import datetime
from typing import List


class MagicedenCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # async def collection_autocomplete(
    #     self,
    #     interaction: discord.Interaction,
    #     current: str,
    # ) -> List[app_commands.Choice[str]]:

    #     fruits = {'fruit1': 'banana', 'adae': 'orange', "kogi": "apple"}
    #     return [
    #         app_commands.Choice(value=fruits[fruit], name=fruit)
    #         for fruit in fruits.keys() if current.lower() in fruit.lower()
    #     ][:25]

    @app_commands.command()
    # @app_commands.autocomplete(collection=collection_autocomplete)
    async def me(self, interaction: discord.Interaction, collection: str):
        """Get collection details from Magiceden marketplace"""
        magiceden = Magiceden()
        collection_details = magiceden.get_collection_details(collection)
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
            embed.add_field(
                name="Try", value="Checking collection on coralcube")
            embed.set_image(
                url="https://c.tenor.com/8RRUPtXrEcgAAAAS/osita-osita-iheme.gif")
            embed.set_footer(text="Built by grim.reaper#9626",
                             icon_url=collection_details[1])

            await interaction.response.send_message(embed=embed)

    @me.error
    async def on_me_error(self, interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
        owner = self.bot.get_user(741308876204408854)
        await interaction.response.send_message("An error occured. Contact grim.reaper#9626 with the command", ephemeral=True)
        await owner.send(f"{error}\n{interaction.data}")


async def setup(bot):
    await bot.add_cog(MagicedenCog(bot))
