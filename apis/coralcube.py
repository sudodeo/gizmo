import requests


class Coralcube:
    def __init__(self) -> None:
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        self.logo = "https://coralcube.io/favicon.ico"
        self.symbol = "◎"
        self.base = "https://coralcube.io/collection/"

    def get_collection_details(self, collection: str):
        fmt_collection = collection.strip().replace(" ","_")
        url = f"https://api.coralcube.io/v1/getItems?page_size=1&symbol={fmt_collection}"

        res = requests.get(url, headers=self.headers)

        print(res.elapsed.total_seconds())
        res_json = res.json()
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
        floor_price = collection_data.get('floor_price') / 1000000000
        listed_count = collection_data.get('listed_count')
        total_supply = collection_data.get('total_count')
        unique_holders = collection_data.get('unique_owners')
        seven_day_volume = collection_data.get('volume') / 1000000000
        # avgPrice24hr = collection_data.get('avgPrice24hr') / 1000000000

        collection_dictionary = {"name": name,
                                 "image": image_url,
                                 "collection_coralcube_url": f"{self.base}{fmt_collection}",
                                 "coralcube_logo": self.logo,
                                 "collection website": collection_website,
                                 "twitter link": twitter_url,
                                 "discord server": discord_url,
                                 "stats": {"total supply": total_supply,
                                           "floor price": f"{floor_price} {self.symbol}",
                                           "listed count": listed_count,
                                           "total volume": f"{seven_day_volume:.2f} {self.symbol}",
                                        #    "avg price 24hr": f"{avgPrice24hr:.2f} {self.symbol}",
                                           "unique holders": unique_holders}
                                 }
        return collection_dictionary