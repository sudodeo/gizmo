import random
import requests
import timeit
import aiohttp


class Magiceden:
    def __init__(self) -> None:
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        self.logo = "https://magiceden.io/img/favicon/android-chrome-192x192.png"
        self.symbol = "◎"
        self.base = "https://magiceden.io/marketplace/"
        self.lamport = 1000000000
        self.user_agents = [
            'Windows 10/ Edge browser: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
            'Windows 7/ Chrome browser: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/47.0.2526.111 Safari/537.36',
            'Mac OS X10/Safari browser: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, '
            'like Gecko) Version/9.0.2 Safari/601.3.9',
            'Linux PC/Firefox browser: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
            'Chrome OS/Chrome browser: Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/51.0.2704.64 Safari/537.36']

    async def get_collection_details(self, collection: str):
        fmt_collection = collection.strip().lower().replace(" ", "_")
        url = f'https://api-mainnet.magiceden.dev/v2/collections/{fmt_collection}'
        # print(url)
        session = aiohttp.ClientSession()
        async with session.get(url, headers={'User-Agent': random.choice(self.user_agents)}) as res:
            # res = requests.get(url, headers=self.headers)
            # print(res.elapsed.total_seconds())
            res_json = await res.json()
            if type(res_json) == str:
                return None, self.logo
            # Basic info
            name = res_json.get('name')
            image_url = res_json.get('image')
            # description = res_json.get('description')
            discord_url = res_json.get("discord")
            collection_website = res_json.get('website')
            # print(collection_website)
            twitter_url = res_json.get('twitter')

            # Stats
            floor_price = res_json.get('floorPrice')
            listed_count = res_json.get('listedCount')
            total_volume = res_json.get('volumeAll')
            avgPrice24hr = res_json.get('avgPrice24hr')

            # GET TOTAL SUPPLY AND UNIQUE HOLDERS
            # url = f'https://api-mainnet.magiceden.io/rpc/getCollectionHolderStats/{fmt_collection}'
            # res = requests.get(url, headers=self.headers)
            # res_json = res.json().get("results")
            # total_supply = res_json.get('totalSupply')
            # unique_holders = res_json.get('uniqueHolders')

            if floor_price == None:
                floor_price = 0
            if total_volume == None:
                total_volume = 0
            if avgPrice24hr == None:
                avgPrice24hr = 0
            collection_dictionary = {"name": name,
                                     "image": image_url,
                                     "collection_magiceden_url": f"{self.base}{fmt_collection}",
                                     "magiceden logo": self.logo,
                                     "collection website": collection_website,
                                     "twitter link": twitter_url,
                                     "discord server": discord_url,
                                     "stats": {"floor price": f"{floor_price / self.lamport} {self.symbol}",
                                               "listed count": listed_count,
                                               "total volume": f"{(total_volume / self.lamport):.2f}{self.symbol}",
                                               "avg price 24hr": f"{(avgPrice24hr / self.lamport):.2f}{self.symbol}", }
                                     }
        await session.close()

        return collection_dictionary

    async def get_popular_collections(self, timeframe=24):
        # Avaialable timeframes: 5m, 15m, 1h, 6h, 24h, 7d, 30d
        if timeframe not in [5, 15, 1, 6, 24, 7, 30]:
            return "Unavailable timeframe"
        time_keys = {5: "top5m", 15: "top15m", 1: "top1h",
                     6: "top6h", 24: "top24h", 7: "top7d", 30: "top30d"}
        url = f'https://stats-mainnet.magiceden.io/collection_stats/popular_collections'
        session = aiohttp.ClientSession()
        async with session.get(url, headers=self.headers) as res:
            # res = requests.get(url, headers=self.headers)
            res_json = await res.json().get(time_keys.get(timeframe))
        # Response example for 5 minutes:
        # {
        #     "collectionSymbol": "infected_mob",
        #     "name": "Infected Mob",
        #     "image": "https://bafybeifqhkedp652y26ks7epgzorf33wktky6e4pf7pn6gfivrd4nkmrs4.ipfs.nftstorage.link/",
        #     "ownerCount": 2505,
        #     "tokenCount": 7777,
        #     "vol": 6.199,
        #     "txns": 2,
        #     "avgPrice": 3.0995,
        #     "volDelta": 1.0246280991735537,
        #     "txnsDelta": 1,
        #     "avgPriceDelta": 1.0246280991735537,
        #     "fp": 3099000000,
        #     "fpDelta": 1,
        #     "rank": 1,
        #     "description": "A science experiment gone completely wrong. 7777 deranged and savage mobsters wreaking havoc in the streets of Solana."
        # }
        await session.close()
        # return res_json

    async def wallet_tracker(self, wallet: str):
        url = f"https://api-mainnet.magiceden.dev/v2/wallets/{wallet}/activities?offset=0&limit=10"
        session = aiohttp.ClientSession()
        async with session.get(url, headers=self.headers) as res:
            res_json = await res.json()
            # ERROR
        # {
        #     "errors": [
        #         {
        #             "value": "ade",
        #             "msg": "invalid wallet_address",
        #             "param": "wallet_address",
        #             "location": "params"
        #         }
        #     ]
        # }
            mint_token = res_json.get("tokenMint")
            transaction_type = res_json.get("type")
            transaction_signature = res_json.get("signature")
            symbol = res_json.get("collectionSymbol")
            buyer = res_json.get("buyer")
            seller = res_json.get("seller")
            price = res_json.get("price")
            token_url = f"https://api-mainnet.magiceden.dev/v2/tokens/{mint_token}"
            async with session.get(token_url, headers=self.headers) as res2:
                res2_json = await res2.json()
                nft_name = res2_json.get("name")
                nft_image = res2_json.get("image")
        # GET TOKEN AFTER REQUEST
        # https://api-mainnet.magiceden.dev/v2/tokens/CcYH3HBXfUrPW74Dy457yXxLwuAiAoot7ZvS23vSc1YG

        async def mint_tracker(self, collection: str):
            fmt_collection = collection.strip().lower().replace(" ", "_")
            
# me = Magiceden()
# print(me.get_collection_details("chimpnana"))
# print(str(timeit.timeit('(me.get_collection_details("chimpnana"))', setup='from __main__ import me')))


# api-devnet.magiceden.dev/v2/collections?offset=0&limit=200
