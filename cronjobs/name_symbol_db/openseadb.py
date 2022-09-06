#! /usr/bin/python3

import logging
import pathlib
import random
import asyncpg
from aiohttp import ClientSession
import asyncio
from decouple import config
from asyncpg.exceptions import UniqueViolationError

root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
log_path = pathlib.Path.cwd().joinpath('opensea_name_symbol_db.log')
handler = logging.FileHandler(
    str(log_path), 'a', 'utf-8')
root_logger.addHandler(handler)


class Opensea:
    POSTGRES_URI = config('POSTGRES_URI')

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
        self.conn = await asyncpg.connect(self.POSTGRES_URI)

        await self.conn.execute('''
        CREATE TABLE IF NOT EXISTS opensea(
        id serial PRIMARY KEY,
        symbol text UNIQUE,
        name text
        );
        ''')

        return await self.scrape_collections()

    async def scrape_collections(self):
        res_json = ""

        while res_json != []:
            url = f"https://api.opensea.io/api/v1/collections?offset={self.offset}&limit=250"

            async with ClientSession() as session:
                async with session.get(url, headers={'user-agent': random.choice(self.user_agents)}) as res:
                    if res.status != 200:
                        logging.error(
                            f"Error fetching data from {url}: {res.status}")
                        await self.conn.execute('''
                        CREATE UNIQUE INDEX IF NOT EXISTS opensea_name_idx ON opensea (name, symbol);
                        ''')
                        await self.close_database()
                        break
                    res_json = await res.json()

                    collections = res_json.get('collections')
                    if collections == []:
                        logging.info(
                            f"Finished scraping {self.offset} collections")
                        await self.conn.execute('''
                        CREATE UNIQUE INDEX IF NOT EXISTS opensea_name_idx ON opensea (name, symbol);
                        ''')
                        await self.close_database()
                        break

                    for nft_collection in collections:
                        symbol = nft_collection.get("slug")
                        unique_holders = nft_collection.get(
                            "stats").get('num_owners')
                        if "autogen" in symbol or "untitled" in symbol:
                            continue
                        if unique_holders <= 1:
                            continue
                        name = nft_collection.get("name")

                        try:
                            await self.conn.execute('''
                            INSERT INTO opensea(symbol, name) VALUES($1, $2)
                            ON CONFLICT (symbol) DO NOTHING''', symbol, name)

                        except Exception as e:
                            logging.error(
                                f"Error inserting {symbol} into database: {e}")
                            continue
                    # print(f"uploading {self.offset}")

                    # 300 is the limit but i'm using 250 because i feel like it's more efficient, i don't know lol
                    self.offset += 250

        return await self.close_database()

    async def close_database(self):
        await self.conn.close()


os = Opensea()
asyncio.run(os.connect_database())
