import discord
from discord.ext import commands
from decouple import config
import interactions
# from discord_slash.utils.manage_commands import create_option
from opensea import Opensea
from dictionary import AntiBozo
from magiceden import Magiceden

from dictionary import AntiBozo

bot_prefix = "?"

_TOKEN = config('DISCORD_TOKEN')


class Client(discord.Client):
    async def on_ready(self):
        print(f"Bot online")
        

    async def on_message(self, message):
        if message.content.startswith(bot_prefix):
            if message.content.startswith(f"{bot_prefix}opensea"):
                collection = message.content.split(" ")[1]
                collection_details = Opensea().get_collection_details(collection)
                if type(collection_details) == dict:
                    name, logo, image, opensea_url, website, twitter, discord_server, stats = collection_details.values()
                    # print(stats)
                    # print(collection_details)
                    embed = discord.Embed(title=name, url=opensea_url, color=0x00ff00)
                    # embed.add_field(name="Name", value=name, inline=False)
                    # embed.add_field(name="website", value=website, inline=True)
                    # embed.add_field(name="twitter", value=twitter, inline=True)
                    # embed.add_field(name="discord", value=discord_server, inline=True)
                    embed.add_field(name="Floor Price", value=stats.get("floor price"), inline=False)
                    embed.add_field(name="Total Supply", value=int(stats.get("total supply")), inline=False)
                    embed.add_field(name="Total Volume", value=stats.get("total volume"), inline=False)
                    embed.add_field(name="Avg Price 24hr", value=stats.get("avg price 24hr"), inline=False)
                    embed.add_field(name="Unique Holders", value=stats.get("unique holders"), inline=False)
                    embed.set_thumbnail(url=logo)
                    embed.set_image(url=image)
                    embed.set_footer(text="Powered by OpenSea, Built by grim.reaper#9626")
                    # print(collection)
                    await message.channel.send(embed=embed)
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
                    await message.channel.send(embed=embed)
            
            elif message.content.startswith(f"{bot_prefix}magiceden"):
                collection = message.content.split("?magiceden")[1]
                collection_details = Magiceden().get_collection_details(collection)

                if type(collection_details) == dict:
                    # print(collection_details)
                    name, image, logo, website, twitter, discord_server, stats = collection_details.values()
                    # print(stats)
                    embed = discord.Embed(title=name, color=0x00ff00)
                    # embed.add_field(name="Name", value=name, inline=False)
                    # embed.add_field(name="website", value=website, inline=True)
                    # embed.add_field(name="twitter", value=twitter, inline=True)
                    # embed.add_field(name="discord", value=discord_server, inline=True)
                    embed.add_field(name="Floor Price", value=stats.get("floor price"), inline=False)
                    # embed.add_field(name="Total Supply", value=stats.get("total supply"), inline=False)
                    embed.add_field(name="Total Volume", value=stats.get("total volume"), inline=False)
                    embed.add_field(name="Avg Price 24hr", value=stats.get("avg price 24hr"), inline=False)
                    embed.add_field(name="Listed NFTs", value=stats.get("listed count"), inline=False)
                    embed.set_thumbnail(url=logo)
                    embed.set_image(url=image)
                    embed.set_footer(text="Powered by Magiceden, Built by grim.reaper#9626", icon_url=logo)
                    # print(collection)
                    await message.channel.send(embed=embed)
                # opensea = Opensea()
                # collection_dictionary = opensea.get_floor_price(collection)
                # await message.channel.send(embed=collection_dictionary)
                else:
                    # print(collection_details)
                    embed = discord.Embed(title="Collection not found", color=0xFF0000)
                    embed.set_thumbnail(url=collection_details[1])
                    embed.set_image(url="https://c.tenor.com/8RRUPtXrEcgAAAAS/osita-osita-iheme.gif")
                    embed.set_footer(text="Powered by OpenSea, Built by grim.reaper#9626")
                    await message.channel.send(embed=embed)
client = Client()
# client = interactions.Client(_TOKEN)
# slash = SlashCommand(client, sync_commands=True)


# @client.command(name='search',
#              description='Search for a word in the dictionary',
#              options=[interactions.Option(
#                  name='word',
#                  description='The word to search for',
#                  required=True,
#                  type=interactions.OptionType.STRING
#              )],
#              scope=['935741302769844244'])
# async def search(ctx: interactions.CommandContext, word):
#     dictionary = AntiBozo()
#     definition, part_of_speech = dictionary.word_search(word)
#     print(definition)
#     if definition:
#         embed = discord.Embed(title=f"{word}", description=f"{definition}", color=0x00ff00)
    
#         embed.set_footer(text=f"{part_of_speech}")

#         await ctx.send(embeds=embed)
#     else:
#         print("No definition found") 

# client.start()

@commands.command(name='os')
async def os(ctx: commands.Context, collection: str):
    opensea = Opensea()
    name, logo, image, website, twitter, discord_server, stats = opensea.get_floor_price(collection).values()

    embed = discord.Embed(title="OpenSea", description="OpenSea is a decentralized marketplace for digital assets. It is a decentralized exchange for digital assets that is powered by the Ethereum blockchain.", color=0x00ff00)
    # embed.add_field(name="Name", value=name, inline=True)
    embed.add_field(name="website", value=website, inline=False)
    embed.add_field(name="twitter", value=twitter, inline=False)
    embed.add_field(name="discord", value=discord_server, inline=False)
    embed.set_thumbnail(url=logo)
    embed.seT_image(url=image)
    embed.set_footer(text="https://opensea.io")
    await ctx.send(embed=embed)

client.run(_TOKEN)
 
