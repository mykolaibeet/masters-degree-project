from sqlalchemy import Column, Integer, String, Numeric, DateTime, Boolean, Sequence, UniqueConstraint, JSON, \
    ForeignKey, BigInteger, Float
from sqlalchemy.sql import func
# from common.db import Base

from sqlalchemy.orm import declarative_base, relationship

from config import SCHEMA

Base = declarative_base()

# table_name = "tokens"
# breakpoint()
class Token(Base):
    __tablename__ = 'tokens'
    __table_args__ = {'schema': SCHEMA}

    # id = Column(Integer, Sequence(f'{__tablename__}_id_seq', schema=SCHEMA), primary_key=True, nullable=False)
    id = Column(String, Sequence(f'{__tablename__}_id_seq', schema=SCHEMA), primary_key=True, nullable=False)
    name = Column(String, unique=True, nullable=False)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    modified_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    activities = relationship('Activity', back_populates='token')
    # score = Column(Integer, CheckConstraint('your_column > 0 AND your_column < 100'))
    # min_value = Column(Numeric(10, 2))
    # max_value = Column(Numeric(10, 2))
    # units = Column(String(20))


class Activity(Base):
    __tablename__ = 'activities'
    __table_args__ = {'schema': SCHEMA}

    id = Column(Integer, Sequence(f'{__tablename__}_id_seq', schema=SCHEMA), primary_key=True, nullable=False)
    signature = Column(String, nullable=False)
    type = Column(String, nullable=False)
    source = Column(String, nullable=False)
    token_mint = Column(String, ForeignKey(f'{SCHEMA}.tokens.id'), nullable=False)
    collection_symbol = Column(String)
    slot = Column(Integer, nullable=False)
    block_time = Column(Integer, nullable=False)
    buyer = Column(String)
    buyer_referral = Column(String)
    seller_referral = Column(String)
    price = Column(Float, nullable=False)
    image = Column(String)

    # Define a foreign key relationship to PriceInfo
    price_info_id = Column('price_info_id', Integer, ForeignKey(f'{SCHEMA}.price_info.id'), nullable=False)
    # price_info = Column(JSON)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    modified_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    token = relationship('Token', back_populates='activities')
    price_info = relationship('PriceInfo', back_populates='activity')


class PriceInfo(Base):
    __tablename__ = 'price_info'
    __table_args__ = {'schema': SCHEMA}

    id = Column(Integer, Sequence(f'{__tablename__}_id_seq', schema=SCHEMA), primary_key=True, nullable=False)
    # activity_id = Column(String, ForeignKey('activities.id'), unique=True, nullable=False)
    raw_amount = Column(String, nullable=False)
    address = Column(String, nullable=False)
    decimals = Column(Integer, nullable=False)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    modified_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    activity = relationship('Activity', back_populates='price_info')