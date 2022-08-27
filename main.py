from typing import Literal, Optional
from discord.ext import commands, tasks
# from settings import *
import asyncpg
import discord
import logging
from discord import app_commands
from decouple import config
import asyncio
import os
import aiohttp


DISCORD_BOT_TOKEN = config('DISCORD_BOT_TOKEN')

# handler = logging.FileHandler(filename='gizmo.log', encoding='utf-8', mode='a')
MY_GUILD = discord.Object(id=935741302769844244)


class MyBot(commands.Bot):
    POSTGRES_URI = config('POSTGRES_URI')
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(command_prefix=commands.when_mentioned_or('>'), intents=intents)
        # self.initial_extensions = [
        #     'cogs.',
        #     'cogs.foo',
        #     'cogs.bar',
        # ]
        # self.tree = app_commands.CommandTree(self)


    async def setup_hook(self):
        # self.background_task.start()
        self.loop.create_task(self.startup())
        self.session = aiohttp.ClientSession()
        self.conn = await asyncpg.connect(self.POSTGRES_URI)

        for file_name in os.listdir("./cogs"):

            if file_name.endswith(".py") and file_name != "__init__.py":
                await bot.load_extension(f"cogs.{file_name[:-3]}")

        @bot.command()
        @commands.is_owner()
        @commands.guild_only()
        async def sync(
        ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
            if not guilds:
                if spec == "~":
                    synced = await ctx.bot.tree.sync(guild=MY_GUILD)
                elif spec == "*":
                    ctx.bot.tree.copy_global_to(guild=MY_GUILD)
                    synced = await ctx.bot.tree.sync(guild=MY_GUILD)
                elif spec == "^":
                    ctx.bot.tree.clear_commands(guild=MY_GUILD)
                    await ctx.bot.tree.sync(guild=MY_GUILD)
                    synced = []
                else:
                    synced = await ctx.bot.tree.sync()
                              
                await ctx.send(
                    f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
                )

                await self.get_user(self.owner_id).send(f"{synced}")
                return
            
            ret = 0
            for guild in guilds:
                try:
                    await ctx.bot.tree.sync(guild=guild)
                except discord.HTTPException:
                    pass
                else:
                    ret += 1

            await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

        # self.tree.copy_global_to(guild=MY_GUILD)
        # await self.tree.sync(guild=MY_GUILD)


    async def close(self):
        await super().close()
        await self.session.close()

    # @tasks.loop(minutes=10)
    # async def background_task(self):
    #     await self.change_presence(activity=discord.Activity(name=f">help ({len(self.guilds)} servers)", type=3))
    #     print('Running background task...')
    @tasks.loop(minutes=30)
    async def startup(self):
        await self.wait_until_ready()
        await self.change_presence(activity=discord.Activity(name=f">help on {len(self.guilds)} servers", type=3))

    async def on_ready(self):
        print('Bot is online!')


bot = MyBot()

bot.run(DISCORD_BOT_TOKEN, )#, log_handler=handler, log_level=logging.DEBUG)
