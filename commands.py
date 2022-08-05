from click import command
from discord.ext import commands
from dictionary import AntiBozo
from decouple import config

_TOKEN = config('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='?')

@commands.command()
async def search(ctx):
    """Search for a word in the dictionary."""
    await ctx.send(AntiBozo().word_of_the_day())


bot.add_command(search)

bot.run(_TOKEN)