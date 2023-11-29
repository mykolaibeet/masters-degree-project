import asyncio
import aiohttp

from datetime import datetime
from pprint import pprint

import requests
import logging

from jsonrpcserver import Success, method, serve
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from urllib.parse import urlparse, parse_qs
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from sqlalchemy.orm import sessionmaker


# from common.db import get_or_create
from config import SOURCE_API_URL, DATABASE_ASYNC_URL
from models import Token, Activity, PriceInfo
from service import add_token, add_activities, get_collection

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class MagicEdenAPI:
    def __init__(self, token_mint: str):
        self.base_url = SOURCE_API_URL
        self.token_mint = token_mint

    async def get_collections(self):
        url = f"{self.base_url}/collections"
        collections = {}
        is_not_empty = True
        limit = 500
        start = 0
        stop = 10 * limit
        process_again = []
        while is_not_empty or process_again:
            async with aiohttp.ClientSession() as session:
                result = []
                tasks = [
                    session.get(url, params={'limit': limit, 'offset': offset}) for offset in range(start, stop, limit)
                ] if is_not_empty else process_again
                responses = await asyncio.gather(*tasks)
                for response in responses:
                    if response.status == 200:
                        result.append(await response.json())
                        response.close()
                    else:
                        logger.warning(f'Failed to process {str(response.url)}, url will be processed again')
                        process_again.append(str(response.url))

                start = stop
                stop += 10 * limit
                is_not_empty = all(result)
                for page in result:
                    for item in page:
                        collections[item['symbol']] = item
        return collections



    async def get_metadata(self):
        url = f"{self.base_url}/tokens/{self.token_mint}"
        # if limit or offset:
        #     url = f'{url}?{"&".join([f"{k}={v}" for k, v in {"offset": offset, "limit": limit}.items()])}'
        # breakpoint()
        response = requests.get(url)
        # breakpoint()
        if response.status_code == 200:
            try:
                metadata = response.json()
            except Exception:
                return []
            else:
                return metadata
        else:
            logger.error(f"Failed to retrieve metadata for {self.token_mint}. Status code: {response.status_code}")
            return None

    async def get_token_activities(self):
        url = f"{self.base_url}/tokens/{self.token_mint}/activities"
        response = requests.get(url)
        if response.status_code == 200:
            try:
                activities = response.json()
            except Exception:
                return []
            else:
                return activities
        else:
            logger.error(f"Failed to retrieve activities for {self.token_mint}. Status code: {response.status_code}")
            return None

    async def process(self):
        logger.info(f'Getting info for {self.token_mint}')
        metadata, activities = await asyncio.gather(self.get_metadata(), self.get_token_activities())
        # breakpoint()
        async_session = get_session(DATABASE_ASYNC_URL)
        async with async_session() as session:
            async with session.begin():
                collection = await get_collection(session, metadata['collection'])
                # breakpoint()


        # token, is_created = get_or_create(session, Token, token_mint=metadata['mintAddress'])
        # token = await add_token(metadata, session)
        # activities = await add_activities(activities, session)
        # try:
        #     await session.commit()
        #     # return city
        # except IntegrityError as ex:
        #     await session.rollback()
        # raise DuplicatedEntryError("The city is already stored")
        buy_now_activities = filter(lambda x: x['type'] == 'buyNow', activities)
        latest_bid_activity = next(filter(lambda x: x['type'] == 'bid', activities))
        # breakpoint()

        dates = []
        prices = []

        for activity in buy_now_activities:
            dates.append(str(datetime.fromtimestamp(activity['blockTime'])))
            prices.append(activity['price'])

        dates.reverse()
        prices.reverse()
        # breakpoint()
        return {
            'nft_name': metadata['name'],
            'token_address': metadata['mintAddress'],
            'dates': dates,
            'prices': prices,
            'last_offer': latest_bid_activity['price'],
            'has_discord': int(collection.has_discord),
            'has_website': int(collection.has_website),
            'has_twitter': int(collection.has_twitter),
            'is_badged': int(collection.is_badged),
        }

    # def get_collection_stats(self, collection_id):
    #     url = f"{self.base_url}/collections/{collection_id}/stats"
    #     response = requests.get(url)
    #     if response.status_code == 200:
    #         stats = response.json()
    #         return stats
    #     else:
    #         pprint(f"Failed to retrieve collection stats. Status code: {response.status_code}")
    #         return None

    # def get_collection_listings(self, collection_id):
    #     url = f"{self.base_url}/collections/{collection_id}/listings"
    #     response = requests.get(url)
    #     if response.status_code == 200:
    #         listings = response.json()
    #         return listings
    #     else:
    #         pprint(f"Failed to retrieve collection listings. Status code: {response.status_code}")
    #         return None

    # def get_collection_holder_stats(self, collection_id):
    #     url = f"{self.base_url}/collections/{collection_id}/holder_stats"
    #     response = requests.get(url)
    #     breakpoint()
    #     if response.status_code == 200:
    #         holder_stats = response.json()
    #
    #         return holder_stats
    #     else:
    #         pprint(f"Failed to retrieve holder stats. Status code: {response.status_code}")
    #         return None

# Example usage:

def get_session(database_url: str):
    engine = create_async_engine(database_url, echo=True)
    async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    return async_session


async def get_or_create(session, model, defaults=None, **kwargs):
    instance = await session.query(model).filter_by(**kwargs).one_or_none()
    if instance:
        return instance, False
    else:
        kwargs |= defaults or {}
        instance = model(**kwargs)
        try:
            session.add(instance)
            session.commit()
        except Exception:
            # The actual exception depends on the specific database so we catch all exceptions. This is similar to the official documentation: https://docs.sqlalchemy.org/en/latest/orm/session_transaction.html
            session.rollback()
            instance = session.query(model).filter_by(**kwargs).one()
            return instance, False
        else:
            return instance, True

@method
def process(url: str):
    # api =
    # breakpoint()
    parsed_url = urlparse(url)
    token_mint = parsed_url.path.split('/')[-1]
    data = asyncio.run(MagicEdenAPI(token_mint).process())
    logger.info(f'Response: {data}')
    return Success(data)


# collections = api.get_collections(limit=20)[:1]
# if collections:
#     for collection in collections:
#         collection_id = collection["symbol"]
#         pprint(f"Collection: {collection['name']}")

        # activities = api.get_collection_activities(collection_id)
        # if activities:
        #     pprint(f"Activities: {activities}")

        # stats = api.get_collection_stats(collection_id)
        # if stats:
        #     pprint(f"Stats: {stats}")

        # listings = api.get_collection_listings(collection_id)
        # if listings:
        #     pprint(f"Listings: {listings}")

        # holder_stats = api.get_collection_holder_stats(collection_id)
        # if holder_stats:
        #     pprint(f"Holder Stats: {holder_stats}")

if __name__ == "__main__":

    # token_mint = 'AQj5FVcxDzbgpPNNVLmQnbPKqeCt9wMYG1qqBLdeTRh9'
    # api = MagicEdenAPI(token_mint)
    # asyncio.run(api.process())
    # test = asyncio.run(MagicEdenAPI(token_mint).process())
    # breakpoint()
    serve()
    # test =
    # breakpoint()
