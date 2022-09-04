#!/usr/bin/python3

from datetime import datetime
import random
import asyncpg
import httpx
from aiohttp import ClientSession
import asyncio
import pause
import logging
from decouple import config
from asyncpg.exceptions import UniqueViolationError

# the magic eden rpc endpoint is protected by cloudflare
# and python-requests and aiohttp don't play nice
# with cloudflare because they use HTTP/1.1
# so we need to use HTTP/2 to bypass the protection
# and use a random user agent to avoid being blocked
# Explanation here: https://stackoverflow.com/a/70706028
# Documentation for httpx: https://www.python-httpx.org/http2/


class Magiceden:
    logging.basicConfig(filename='../../magiceden_ath_atl.log', encoding='utf-8',
                        filemode='a', level=logging.INFO, format='%(levelname)s:%(message)s')
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

    async def connect_database(self):
        self.conn = await asyncpg.connect(self.POSTGRES_URI)

        # using magiceden table to store data
        await self.conn.execute('''
        CREATE TABLE IF NOT EXISTS magiceden(
        id serial PRIMARY KEY,
        symbol text UNIQUE,
        name text,
        ATH int,
        ATH_date date,
        ATL int,
        ATL_date date,
        last_scraped_index int
        );
        ''')
        # return the value in the first row from the resulting query
        self.db_rows = await self.conn.fetchval('''
        SELECT count(*) FROM magiceden;
        ''')

        return await self.scrape_collections()

    async def scrape_collections(self):

        for row in range(self.db_rows):
            symbol = await self.conn.fetchval('''
            SELECT symbol FROM magiceden WHERE id = $1;
            ''', row + 1)
            url = f"https://api-mainnet.magiceden.io/rpc/getCollectionTimeSeries/{symbol}?resolution=1d"

            async with httpx.AsyncClient(http2=True) as client:
                res = await client.get(url, headers={'user-agent': random.choice(self.user_agents)})
                if res.status_code != 200:
                    logging.info(f"URL: {url}")
                    logging.error(
                        f"Error while making api request: {res.status_code}")
                    logging.info(f"Response from server: {res.text}")
                    return await self.close_database()

                # response is a list of dictionaries
                res_json = res.json()

                if res_json == []:
                    await self.conn.execute('''
                    CREATE UNIQUE INDEX IF NOT EXISTS nft_name_idx ON magiceden (name, symbol);
                    ''')
                    return await self.close_database()

            ath = 0
            # setting atl to a very high number so that it can be
            # replaced by the first value using the if statement for loop
            atl = 1500000
            ath_date = ""
            atl_date = ""
            last_scraped_index = await self.conn.fetchval('''
            SELECT last_scraped_index FROM magiceden WHERE id = $1;
            ''', row + 1)
            if last_scraped_index == None:
                last_scraped_index = 0

            for index, dictionary in enumerate(res_json[last_scraped_index:]):
                if dictionary['maxFP'] > ath:
                    ath = dictionary['maxFP']
                    # sometimes, the timestamp is in milliseconds instead of seconds
                    # so we need to try to convert it to seconds first
                    try:
                        ath_date = datetime.fromtimestamp(
                            dictionary['ts'])
                    except ValueError:
                        ath_date = datetime.fromtimestamp(
                            dictionary['ts'] / 1000)
                if dictionary['minFP'] < atl:
                    atl = dictionary['minFP']
                    try:
                        atl_date = datetime.fromtimestamp(
                            dictionary['ts'])
                    except ValueError:
                        atl_date = datetime.fromtimestamp(
                            dictionary['ts'] / 1000)
                if index == 0:
                    continue
                last_scraped_index += 1

            #  update the database with the new values
            try:
                await self.conn.execute('''
                UPDATE magiceden
                SET ath = $1, ath_date = $2, atl = $3, atl_date = $4, last_scraped_index = $5
                WHERE symbol = $6;
                ''', ath, ath_date, atl, atl_date, last_scraped_index, symbol)
            except UniqueViolationError:
                logging.error(
                    f"Error: {symbol} already exists in the database")
                return await self.close_database()
            # return print(f"Scraped {symbol}, ath: {ath}, ath_date: {ath_date}, atl: {atl}, atl_date: {atl_date}, last_scraped_index: {last_scraped_index}")
        return await self.close_database()

    async def close_database(self):
        await self.conn.close()


me = Magiceden()
asyncio.run(me.connect_database())
