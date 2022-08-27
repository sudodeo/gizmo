import asyncio
import random
import aiohttp


class Coralcube:
    def __init__(self) -> None:
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
            'Referer': 'https://coralcube.io/'}
        self.logo = "https://coralcube.io/favicon.ico"
        self.symbol = "◎"
        self.lamport = 1000000000
        self.base = "https://coralcube.io/collection/"
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
        url = f"https://api.coralcube.io/v1/getItems?page_size=1&symbol={fmt_collection}"
        session = aiohttp.ClientSession()
        async with session.get(url, headers={'User-Agent': random.choice(self.user_agents), 'Referer': 'https://coralcube.io/'}) as res:
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
            if floor_price == None:
                floor_price = 0
            if seven_day_volume == None:
                seven_day_volume = 0

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

    async def sell_wall(self, collection: str, price: int):
        """Summary:
            Computes the sell wall for a collection at a given price

        Args:
            collection (str): The collection to get the sell wall for
            price (int): The price range to get the sell wall for

        Returns:
            list: [total_listings, listed_count, percentage, floor_price, collection_image, collection_name, collection_url]
        """
        price *= self.lamport
        fmt_collection = collection.strip().lower().replace(" ", "_")
        offset = 0

        url_desc = f"https://api.coralcube.io/v1/getItems?offset={offset}&page_size=50&ranking=price_desc&symbol={fmt_collection}"
        session = aiohttp.ClientSession()
        async with session.get(url_desc, headers={'User-Agent': random.choice(self.user_agents), 'Referer': 'https://coralcube.io/'}) as res:
            res_json = await res.json()
            if res_json.get("detail"):
                await session.close()
                return None
            collection_data = res_json.get("collection")
            name = collection_data.get('name')
            image_url = collection_data.get('image')
            floor_price = collection_data.get("floor_price")
            total_listings = collection_data.get("listed_count")
            items: list = res_json.get("items")
            highest_listed_price: int = items[0].get("price")

            if price > highest_listed_price:
                await session.close()
                return [total_listings, total_listings, 100, floor_price / self.lamport, image_url, name, self.base + fmt_collection]
        wall = 0
        while True:
            url = f"https://api.coralcube.io/v1/getItems?offset={offset}&page_size=50&ranking=price_asc&symbol={fmt_collection}"
            async with session.get(url, headers={'User-Agent': random.choice(self.user_agents), 'Referer': 'https://coralcube.io/'}) as res:
                res_json = await res.json()

                # A bad request will return {"detail": "Collection not found"}
                if res_json.get("detail"):
                    await session.close()
                    return None
                collection_data = res_json.get("collection")
                # Listed NFTs
                floor_price = collection_data.get("floor_price")
                total_listings = collection_data.get("listed_count")
                name = collection_data.get('name')
                image_url = collection_data.get('image')

                if floor_price >= price:
                    await session.close()
                    return [wall, 0, floor_price / self.lamport, image_url, name, self.base + fmt_collection]

                collection_items = res_json.get("items")
                price_list = []

                for item in collection_items:
                    nft_price = item.get("price")
                    if not nft_price:
                        break
                    price_list.append(nft_price)

                # NFTs listed below given price

                length = len(price_list)

                if price_list[-1] < price:
                    wall += length
                    # MOVE TO NEXT PAGE
                    offset += 50
                    continue

                else:
                    # find index of next price if price not in price_list
                    for i in range(len(price_list)):
                        if price_list[i] >= price:
                            wall += i
                            break
                    await session.close()
                    return [total_listings, wall, f"{(wall / total_listings * 100):.2f}", floor_price / self.lamport, image_url, name, self.base + fmt_collection]


# cc = Coralcube()
# collection = "Degods"
# price = 33333
# sell_wall = asyncio.run(cc.sell_wall(collection, price))
# print(sell_wall)
