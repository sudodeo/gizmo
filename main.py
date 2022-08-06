from discord.ext import commands
from settings import * 
import discord
from discord import app_commands
import asyncio
import os
import aiohttp


# intents = discord.Intents.default()
# intents.members = True
# intents.message_content = True
# _TOKEN = config('DISCORD_BOT_TOKEN')

# bot = commands.Bot(command_prefix='?', intents=intents)
MY_GUILD = discord.Object(id=935741302769844244)

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(command_prefix='?', intents=intents)
        self.initial_extensions = [
            'cogs.',
            'cogs.foo',
            'cogs.bar',
        ]
        # self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # self.background_task.start()
        self.session = aiohttp.ClientSession()
        
        
        for file_name in os.listdir("./cogs"):
            if file_name.endswith(".py") and file_name != "__init__.py":
                await bot.load_extension(f"cogs.{file_name[:-3]}")
        # self.tree.copy_global_to(guild=MY_GUILD)
        # await self.tree.sync(guild=MY_GUILD)


    async def close(self):
        await super().close()
        await self.session.close()
    
    # async def load_extensions(self):    
        # for file_name in os.listdir("./cogs"):
        #     if file_name.endswith(".py") and file_name != "__init__.py":
        #         await bot.load_extension(f"cogs.{file_name[:-3]}")

    # @tasks.loop(minutes=10)
    # async def background_task(self):
    #     print('Running background task...')

    async def on_ready(self):
        print('Ready!')

bot = MyBot()
# @bot.tree.command()
# async def pings(interaction: discord.Interaction):
#     """Ping bot"""
#     await interaction.response.send_message(f'Pong!, {interaction.user.mention}')
bot.run(DISCORD_BOT_TOKEN)
# async def load_extensions():    
#     for file_name in os.listdir("./cogs"):
#         if file_name.endswith(".py") and file_name != "__init__.py":
#             await bot.load_extension(f"cogs.{file_name[:-3]}")

# async def main():
#     async with bot:
#         await load_extensions()
#         await bot.run(DISCORD_BOT_TOKEN)

# asyncio.run(main())
# async def on_ready():
    # pass
    # print('kk')
    # await print(f"bot.user.id is online")

# bot.add_listener(on_ready)

