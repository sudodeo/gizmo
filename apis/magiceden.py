import requests
import timeit

class Magiceden:
    def __init__(self) -> None:
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        self.logo = "https://magiceden.io/img/favicon/android-chrome-192x192.png"
        self.symbol = "◎"
        self.base = "https://magiceden.io/marketplace/"

    def get_collection_details(self, collection: str):
        fmt_collection = collection.strip().replace(" ","_")
        url = f'https://api-mainnet.magiceden.dev/v2/collections/{fmt_collection}'
        # print(url)
        res = requests.get(url, headers=self.headers)
        print(res.elapsed.total_seconds())
        res_json = res.json()
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
        floor_price = res_json.get('floorPrice') / 1000000000
        listed_count = res_json.get('listedCount')
        total_volume = res_json.get('volumeAll') / 1000000000
        avgPrice24hr = res_json.get('avgPrice24hr') / 1000000000

        # GET TOTAL SUPPLY AND UNIQUE HOLDERS
        # url = f'https://api-mainnet.magiceden.io/rpc/getCollectionHolderStats/{collection.strip().replace(" ","_")}'
        # res = requests.get(url, headers=self.headers)
        # res_json = res.json().get("results")
        # total_supply = res_json.get('totalSupply')
        # unique_holders = res_json.get('uniqueHolders')

        collection_dictionary = {"name": name,
                                 "image": image_url,
                                 "collection_magiceden_url": f"{self.base}{fmt_collection}",
                                 "magiceden logo": self.logo,
                                 "collection website": collection_website,
                                 "twitter link": twitter_url,
                                 "discord server": discord_url,
                                 "stats": {"floor price": f"{floor_price} {self.symbol}",
                                           "listed count": listed_count,
                                           "total volume": f"{total_volume:.2f}{self.symbol}",
                                           "avg price 24hr": f"{avgPrice24hr:.2f}{self.symbol}", }
                                }
        return collection_dictionary

    def get_popular_collections(self, timeframe=24):
        # Avaialable timeframes: 5m, 15m, 1h, 6h, 24h, 7d, 30d
        if timeframe not in [5, 15, 1, 6, 24, 7, 30]:
            return "Unavailable timeframe"
        time_keys = {5: "top5m", 15: "top15m", 1: "top1h",
                     6: "top6h", 24: "top24h", 7: "top7d", 30: "top30d"}
        url = f'https://stats-mainnet.magiceden.io/collection_stats/popular_collections'
        res = requests.get(url, headers=self.headers)
        res_json = res.json().get(time_keys.get(timeframe))
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
        # return res_json
# me = Magiceden()
# print(me.get_collection_details("chimpnana"))
# print(str(timeit.timeit('(me.get_collection_details("chimpnana"))', setup='from __main__ import me')))

