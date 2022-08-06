import requests


class Opensea:
    def __init__(self) -> None:
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        self.twitter_base = "https://twitter.com/"
        self.opensea_base = "https://opensea.io/collection/"
        self.logo = "https://storage.googleapis.com/opensea-static/Logomark/Logomark-Blue.png"
        self.eth_symbol = "Ξ"
        self.sol_symbol = "◎"

    def get_collection_details(self, collection: str):
        fmt_collection = collection.strip().lower()
        url = f"https://api.opensea.io/api/v1/collection/{fmt_collection}"
        res = requests.get(url, headers=self.headers)
        print(res.elapsed.total_seconds())
        if res.status_code == 404:
            return None, self.logo
        res_json = res.json().get("collection")

        # Basic info
        name = res_json.get('name')
        image_url = res_json.get('image_url')
        # description = res_json.get('description')
        discord_url = res_json.get("discord_url")
        collection_website = res_json.get('external_url')

        twitter_username = res_json.get('twitter_username')
        if twitter_username:
            twitter_url = self.twitter_base + twitter_username.strip()
        else:
            twitter_url = None

        # Stats
        total_supply = res_json.get("stats").get('total_supply')
        floor_price = res_json.get("stats").get('floor_price')
        # listed_count = res_json.get("stats").get('listed_count')
        total_volume = res_json.get("stats").get('total_volume')
        avgPrice24hr = res_json.get("stats").get('one_day_average_price')
        unique_holders = res_json.get("stats").get('num_owners')
        if floor_price == None:
            return None, self.logo
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
        # print(collection_dictionary.values())
        return collection_dictionary

    def get_popular_collections(self):
        pass


# Opensea().get_floor_price("doodles-official")
