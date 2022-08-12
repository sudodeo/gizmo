import random
import asyncpg
import aiohttp
import asyncio
from asyncpg.exceptions import UniqueViolationError


class Coralcube:
    def __init__(self) -> None:

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
        self.offset = 0

    async def connect_database(self):
        self.conn = await asyncpg.connect(
            "postgresql://jiggydeo:jiggydeo@localhost/magiceden")

        await self.conn.execute('''
        CREATE TABLE IF NOT EXISTS nftCollections2 (
            id serial PRIMARY KEY,
            symbol text UNIQUE,
            name text 
        )
    ''')

        return await self.scrape_collections()

    async def scrape_collections(self):
        # empty page will return []
        res_json = ""
        while res_json != []:
            url = f"https://api.coralcube.io/v1/getCollections?offset={self.offset}&page_size=50"

            session = aiohttp.ClientSession()
            async with session.get(url, headers={'user-agent': random.choice(self.user_agents)}) as res:
                if res.status != 200:
                    print(f"Error: {res.status}")
                    await session.close()
                    break
                res_json = await res.json()

                if res_json == []:
                    await session.close()
                    break

                for nft_collection in res_json:

                    symbol = nft_collection.get("symbol")
                    name = nft_collection.get("name")

                    try:
                        await self.conn.execute('''
                        INSERT INTO nftCollections2(symbol, name) VALUES($1, $2)
                        ''', symbol, name)

                    except UniqueViolationError as e:
                        continue

                # print(f"uploading {self.offset}")

                self.offset += 50
            await session.close()

        return await self.close_database()

    async def close_database(self):
        await self.conn.close()


cc = Coralcube()
asyncio.run(cc.connect_database())