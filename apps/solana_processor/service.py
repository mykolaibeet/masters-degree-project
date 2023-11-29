from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Token, Activity, PriceInfo, Collection


async def add_token(metadata: dict, session: AsyncSession):
    token = await session.execute(select(Token).filter(Token.id == metadata['mintAddress']).first())
    if token:
        return token
    else:
        new_token = Token(id=metadata['mintAddress'], name=metadata['name'])
        session.add(new_token)
        return new_token

async def add_activities(activities: list, session: AsyncSession):
    for activity in activities:
        collection_symbol = activity.get('collectionSymbol')
        buyer = activity.get('buyer')
        buyer_referral = activity.get('buyerReferral')
        seller_referral = activity.get('sellerReferral')
        image = activity.get('image')
        new_activity = Activity(
            signature=activity['signature'],
            type=activity['type'],
            source=activity['source'],
            token_mint=activity['tokenMint'],
            collection_symbol=collection_symbol,
            slot=activity['slot'],
            block_time=activity['blockTime'],
            buyer=buyer,
            buyer_referral=buyer_referral,
            seller_referral=seller_referral,
            price=activity['price'],
            image=image,
        )
        new_activity.price_info = PriceInfo(
            raw_amount=activity['priceInfo']['solPrice']['rawAmount'],
            address=activity['priceInfo']['solPrice']['address'],
            decimals=activity['priceInfo']['solPrice']['decimals']
        )
        session.add(new_activity)


async def get_collection(session: AsyncSession, symbol: str) -> Collection:
    result = await session.execute(
        select(Collection).filter(Collection.symbol == symbol)
    )
    return result.scalars().first()
