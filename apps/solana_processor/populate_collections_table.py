import asyncio

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from config import DATABASE_ASYNC_URL
from main import MagicEdenAPI
from models import Collection

async def main():
    collections = await MagicEdenAPI(None).get_collections()
    # breakpoint()
    engine = create_async_engine(DATABASE_ASYNC_URL, echo=True)
    Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    # session = get_session(DATABASE_ASYNC_URL)
    # objects = [
    #     Collection(
    #         symbol=collection['symbol'],
    #         name=collection.get('name', collection['symbol']),
    #         has_website=bool(collection.get('website')),
    #         has_discord=bool(collection.get('discord')),
    #         has_twitter=bool(collection.get('twitter')),
    #         is_badged=bool(collection.get('isBadged'))
    #     )
    #     for collection in collections
    # ]
    # for collection in collections:
    async with Session() as session:
        async with session.begin():
            session.add_all([
                Collection(
                    symbol=symbol,
                    name=collection.get('name', symbol),
                    has_website=bool(collection.get('website')),
                    has_discord=bool(collection.get('discord')),
                    has_twitter=bool(collection.get('twitter')),
                    is_badged=bool(collection.get('isBadged'))
                )
                for symbol, collection in collections.items()
            ])

    # session.run_sync(lambda ses: ses.bulk_insert_mappings(Collection, objects))
        try:
            await session.commit()
        except IntegrityError as ex:
            await session.rollback()
            raise ex
    await engine.dispose()

    # breakpoint()

if __name__ == '__main__':
    asyncio.run(main())