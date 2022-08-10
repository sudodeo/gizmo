import requests
import aiohttp


class Coralcube:
    def __init__(self) -> None:
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        self.logo = "https://coralcube.io/favicon.ico"
        self.symbol = "◎"
        self.lamport = 1000000000
        self.base = "https://coralcube.io/collection/"

    async def get_collection_details(self, collection: str):
        fmt_collection = collection.strip().lower().replace(" ", "_")
        url = f"https://api.coralcube.io/v1/getItems?page_size=1&symbol={fmt_collection}"
        session = aiohttp.ClientSession()
        async with session.get(url, headers=self.headers) as res:
            res_json = await res.json()
            # print(res_json)
            # A bad request will return {"detail": "Collection not found"}
            if res_json.get("detail"):
                return None, self.logo

            # Basic info
            collection_data = res_json.get("collection")

            name = collection_data.get('name')
            image_url = collection_data.get('image')
            # description = res_json.get('description')
            discord_url = collection_data.get("discord")
            collection_website = collection_data.get('website')
            # print(collection_website)
            twitter_url = collection_data.get('twitter')

            # Stats
            floor_price = collection_data.get('floor_price')
            listed_count = collection_data.get('listed_count')
            total_supply = collection_data.get('total_count')
            unique_holders = collection_data.get('unique_owners')
            seven_day_volume = collection_data.get('volume')
            # avgPrice24hr = collection_data.get('avgPrice24hr') / 1000000000
            if None in [floor_price, seven_day_volume]:
                return None, self.logo
            collection_dictionary = {"name": name,
                                     "image": image_url,
                                     "collection_coralcube_url": f"{self.base}{fmt_collection}",
                                     "coralcube_logo": self.logo,
                                     "collection website": collection_website,
                                     "twitter link": twitter_url,
                                     "discord server": discord_url,
                                     "stats": {"total supply": total_supply,
                                               "floor price": f"{floor_price / self.lamport} {self.symbol}",
                                               "listed count": listed_count,
                                               "seven day volume": f"{(seven_day_volume / self.lamport):.2f} {self.symbol}",
                                               #    "avg price 24hr": f"{avgPrice24hr:.2f} {self.symbol}",
                                               "unique holders": unique_holders}
                                     }
        await session.close()
        return collection_dictionary

        # data = await resp.json()
        # if data["items"]:
        #     return self.format_collection_details(data["items"][0])
        # else:
        #     return self.format_collection_details(None)

    async def main(self, collection: str):
        collection_dictionary = await self.get_collection_details(collection)
        return collection_dictionary

    def format_collection_details(self, data: dict):
        if data:
            name = data["name"]
            image = data["image"]
            collection_coralcube_url = self.base + data["symbol"]
            logo = self.logo
            website = data["website"]
            twitter = data["twitter"]
            discord_server = data["discord"]
            stats = data["stats"]
            return name, image, collection_coralcube_url, logo, website, twitter, discord_server, stats
        else:
            return None
