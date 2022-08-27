import random
import aiohttp


class Opensea:
    def __init__(self) -> None:
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        self.twitter_base = "https://twitter.com/"
        self.opensea_base = "https://opensea.io/collection/"
        self.logo = "https://storage.googleapis.com/opensea-static/Logomark/Logomark-Blue.png"
        self.eth_symbol = "Ξ"
        self.sol_symbol = "◎"
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
        url = f"https://api.opensea.io/api/v1/collection/{fmt_collection}"
        # res = requests.get(url, headers=self.headers)

        # print(res.elapsed.total_seconds())
        session = aiohttp.ClientSession()
        async with session.get(url, headers={'User-Agent': random.choice(self.user_agents)}) as res:
            if res.status == 404:
                await session.close()
                return None, self.logo
            res_json = await res.json()

            collection = res_json.get("collection")

            # Basic info
            name = collection.get('name')
            image_url = collection.get('image_url')
            # description = res_json.get('description')
            discord_url = collection.get("discord_url")
            collection_website = collection.get('external_url')

            twitter_username = collection.get('twitter_username')
            if twitter_username:
                twitter_url = self.twitter_base + twitter_username.strip()
            else:
                twitter_url = None

            # Stats
            total_supply = collection.get("stats").get('total_supply')
            floor_price = collection.get("stats").get('floor_price')
            # listed_count = res_json.get("stats").get('listed_count')
            total_volume = collection.get("stats").get('total_volume')
            avgPrice24hr = collection.get("stats").get('one_day_average_price')
            unique_holders = collection.get("stats").get('num_owners')
            if floor_price == None:
                floor_price = '---'
            collection_dictionary = {"name": name,
                                     "opensea_logo": self.logo,
                                     "image": image_url,
                                     "collection_opensea_url": f"{self.opensea_base}{fmt_collection}",
                                     "collection website": collection_website,
                                     "twitter link": twitter_url,
                                     "discord server": discord_url,
                                     "stats": {"total supply": total_supply,
                                               "floor price": f"{floor_price} {self.eth_symbol}",
                                               "total volume": f"{total_volume:.2f} {self.eth_symbol}",
                                               "avg price 24hr": f"{avgPrice24hr:.2f} {self.eth_symbol}",
                                               "unique holders": unique_holders}
                                     }
        await session.close()
        return collection_dictionary

    def get_popular_collections(self):
        pass


# Opensea().get_floor_price("doodles-official")
