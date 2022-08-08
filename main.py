from discord.ext import commands
# from settings import *
import discord
from discord import app_commands
from decouple import config
import asyncio
import os
import aiohttp


DISCORD_BOT_TOKEN = config('DISCORD_BOT_TOKEN')


MY_GUILD = discord.Object(id=935741302769844244)


class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(command_prefix='>', intents=intents, activity=discord.Activity(name=f">help ({len(self.guilds)} servers)", type=3))
        # self.initial_extensions = [
        #     'cogs.',
        #     'cogs.foo',
        #     'cogs.bar',
        # ]
        # self.tree = app_commands.CommandTree(self)


    async def setup_hook(self):
        # self.background_task.start()
        self.session = aiohttp.ClientSession()
        # print(os.listdir())

        for file_name in os.listdir("./cogs"):

            if file_name.endswith(".py") and file_name != "__init__.py":
                await bot.load_extension(f"cogs.{file_name[:-3]}")
        # self.tree.copy_global_to(guild=MY_GUILD)
        # await self.tree.sync(guild=MY_GUILD)


    async def close(self):
        await super().close()
        await self.session.close()

    # @tasks.loop(minutes=10)
    # async def background_task(self):
    #     print('Running background task...')

    async def on_ready(self):
        # await self.change_presence()
        print('Bot is online!')


bot = MyBot()

bot.run(DISCORD_BOT_TOKEN)
