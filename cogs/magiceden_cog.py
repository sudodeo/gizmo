import discord
from discord import app_commands
from discord.ext import commands
from magiceden import Magiceden


class MagicedenCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    async def me(self, interaction: discord.Interaction, collection: str):
        """Get collection details from Magiceden marketplace"""
        magiceden = Magiceden()
        collection_details = magiceden.get_collection_details(collection)
        
        
        if type(collection_details) == dict:
            # print(collection_details)
            
            name, image, collection_magiceden_url, logo, website, twitter, discord_server, stats = collection_details.values()
            # print(stats)
            embed = discord.Embed(title=name, url=collection_magiceden_url, color=0x00ff00)
            embed.add_field(name="website", value=website or "None", inline=True)
            embed.add_field(name="twitter", value=twitter or "None", inline=True)
            embed.add_field(name="discord", value=discord_server or "None", inline=True)
            embed.add_field(name="Floor Price", value=stats.get("floor price") or "None", inline=False)
            # embed.add_field(name="Total Supply", value=stats.get("total supply"), inline=False)
            embed.add_field(name="Total Volume", value=stats.get("total volume") or "None", inline=False)
            embed.add_field(name="Avg Price 24hr", value=stats.get("avg price 24hr") or "None", inline=False)
            embed.add_field(name="Listed NFTs", value=stats.get("listed count")or "None", inline=False)
            embed.set_thumbnail(url=logo)
            embed.set_image(url=image)
            embed.set_footer(text="Powered by Magiceden, Built by grim.reaper#9626", icon_url=logo)
            # print(collection)
            # async with ctx.typing():
                # await embed
                # print(embed)
            await interaction.response.send_message(embed=embed)
        # opensea = Opensea()
        # collection_dictionary = opensea.get_floor_price(collection)
        # await message.channel.send(embed=collection_dictionary)
        else:
            # print(collection_details)
            embed = discord.Embed(title="Collection not found", color=0xFF0000)
            embed.set_thumbnail(url=collection_details[1])
            embed.set_image(url="https://c.tenor.com/8RRUPtXrEcgAAAAS/osita-osita-iheme.gif")
            embed.set_footer(text="Powered by Magiceden, Built by grim.reaper#9626", icon_url=collection_details[1])
            # async with ctx.typing():
                # await embed
            await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(MagicedenCog(bot))