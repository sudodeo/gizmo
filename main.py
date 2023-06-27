from ast import arg
import pathlib
from typing import Literal, Optional
from discord.ext import commands, tasks
import asyncpg
import discord
import logging
from discord import app_commands
from decouple import config
import asyncio
import os
import aiohttp

directory_path = os.path.dirname(os.path.abspath(__file__))
DISCORD_BOT_TOKEN = config('DISCORD_BOT_TOKEN')
log_path = f"{directory_path}/gizmo.log"
handler = logging.FileHandler(filename=str(log_path), encoding='utf-8', mode='a')
log = logging.getLogger('gizmo')

MY_GUILD = discord.Object(id=int(config('GUILD_ID')))


class Gizmo(commands.Bot):
    POSTGRES_URI = config('POSTGRES_URI')

    def __init__(self):
        intents = discord.Intents(
            guilds=True,
            members=True,
            bans=True,
            emojis=True,
            voice_states=True,
            messages=True,
            reactions=True,
            message_content=True,
        )
        super().__init__(command_prefix=commands.when_mentioned_or('>'), intents=intents)
        self.initial_extensions = [
            'cogs.coralcube',
            'cogs.dictionary',
            'cogs.magiceden',
            'cogs.opensea',
            'cogs.sell_wall',
            'cogs.test',
        ]
        self.owner = self.get_user(self.owner_id)
        # self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # self.background_task.start()
        self.loop.create_task(self.startup())
        self.session = aiohttp.ClientSession()
        self.conn = await asyncpg.connect(self.POSTGRES_URI)

        for extension in self.initial_extensions:
            try:
                await self.load_extension(extension)
            except Exception:
                log.exception('Failed to load extension %s.', extension)

        @self.command()
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

                await self.owner.send(f"{synced}")
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

    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.author.send('This command cannot be used in private messages.')
        elif isinstance(error, commands.DisabledCommand):
            await ctx.author.send('Sorry. This command is disabled and cannot be used.')
        elif isinstance(error, commands.CommandInvokeError):
            original = error.original
            if not isinstance(original, discord.HTTPException):
                log.exception(
                    'In %s:', ctx.command.qualified_name, exc_info=original)
        elif isinstance(error, commands.ArgumentParsingError):
            await ctx.send(str(error))

    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return
        if message.content.find('deez nuts') != -1:
            await message.reply('https://tenor.com/view/deez-nuts-laughing-funny-haha-gif-4057737')
            await message.channel.send(f"GG <@{message.author.id}>!")
        else:
            await self.invoke(await self.get_context(message))

    async def close(self):
        await super().close()
        await self.session.close()

    @tasks.loop(minutes=30)
    async def startup(self):
        await self.wait_until_ready()
        for guild in self.guilds:
            await self.owner.send(guild)
            asyncio.sleep(1)
        await self.change_presence(activity=discord.Activity(name=f">help on {len(self.guilds)} servers", type=3))

    async def on_ready(self):
        print('Bot is online!')


def main():
    bot = Gizmo()
    bot.run(DISCORD_BOT_TOKEN, log_handler=handler, log_level=logging.WARNING)


main()
