import discord 
from discord import app_commands
from discord.ext import commands
from opensea import Opensea


class OpenseaCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    async def os(self, interaction: discord.Interaction, collection: str):
        """Get collection details from Opensea marketplace"""
        collection_details = Opensea().get_collection_details(collection)
        if type(collection_details) == dict:
            name, logo, image, opensea_url, website, twitter, discord_server, stats = collection_details.values()
            # print(stats)
            # print(collection_details)
            embed = discord.Embed(title=name, url=opensea_url, color=0x00ff00)
            # embed.add_field(name="Name", value=name, inline=False)
            embed.add_field(name="website", value=website, inline=True)
            embed.add_field(name="twitter", value=twitter, inline=True)
            embed.add_field(name="discord", value=discord_server, inline=True)
            embed.add_field(name="Floor Price", value=stats.get("floor price"), inline=False)
            embed.add_field(name="Total Supply", value=int(stats.get("total supply")), inline=False)
            embed.add_field(name="Total Volume", value=stats.get("total volume"), inline=False)
            embed.add_field(name="Avg Price 24hr", value=stats.get("avg price 24hr"), inline=False)
            embed.add_field(name="Unique Holders", value=stats.get("unique holders"), inline=False)
            embed.set_thumbnail(url=logo)
            embed.set_image(url=image)
            embed.set_footer(text="Powered by OpenSea, Built by grim.reaper#9626", icon_url=logo)
            # print(collection)
            await interaction.response.send_message(embed=embed)
        # opensea = Opensea()
        # collection_dictionary = opensea.get_floor_price(collection)
        # await message.channel.send(embed=collection_dictionary)
        else:
            # print(collection_details)
            embed = discord.Embed(title="Collection not found", color=0xFF0000)
            embed.set_thumbnail(url=collection_details[1])
            embed.add_field(name="Try", value="Check spelling", inline=False)
            embed.add_field(name="Try", value="compound name collections should look like:\nboredapeyachtclub or mutant-ape-yacht-club", inline=False)
            embed.set_image(url="https://c.tenor.com/8RRUPtXrEcgAAAAS/osita-osita-iheme.gif")
            embed.set_footer(text="Powered by OpenSea, Built by grim.reaper#9626", icon_url=collection_details[1])
            await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(OpenseaCog(bot))