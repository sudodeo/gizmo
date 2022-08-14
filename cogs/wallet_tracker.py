import discord
from discord import app_commands
from discord.ext import commands, tasks
from apis.magiceden import Magiceden


class WalletTracker(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.wallets = {}

    @commands.hybrid_command()
    async def watch_wallet(self, ctx: commands.Context, name: str, wallet: str) -> None:
        """Add a wallet to the wallet tracker"""
        magiceden = Magiceden()
        await ctx.send(f'{name} has {wallet}')
        cached_transaction_json = await magiceden.wallet_tracker(wallet)
        for wallet_ in self.wallets.keys():
            if wallet not in wallet_.split('_')[1]:
                self.wallets.update({f"{name}_{wallet}": cached_transaction_json})
        else:
            await ctx.send('That wallet is already being tracked')
        # self.bot.loop.create_task(self.wallet_tracker.add_wallet(name, wallet))

    @tasks.loop(minutes=5)
    async def wallet_tracker(self, ctx: commands.Context) -> None:
        magiceden = Magiceden()
        
        for wallet in self.wallets.keys():
            name = wallet.split('_')[0]
            embed = discord.Embed(title=name)
            transaction_json = await magiceden.wallet_tracker(wallet)
            for transaction in transaction_json:
                if transaction not in self.wallets.get(wallet):
                    embed.add_field("transaction", transaction)
                    await ctx.send(embed=embed)
            self.wallets.update({wallet: transaction_json})
    
    @app_commands.command()
    async def unwatch_wallet(self, ctx: commands.Context, name: str, wallet: str) -> None:
        """Remove a wallet from the wallet tracker"""
        await ctx.send(f'{name} has {wallet}')
        try:
            self.wallets.pop(wallet)    
        except KeyError:
            await ctx.send('That wallet is not being tracked')
    
    @watch_wallet.error
    async def watch_wallet_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        """Wallet error"""
        await ctx.send(f'Error: {error}')