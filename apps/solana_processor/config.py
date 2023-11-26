import os

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_PORT = os.getenv('DB_PORT')

DATABASE_URL=f'postgresql://{DB_USER}:{DB_PASSWORD}@db:{DB_PORT}/{DB_NAME}'
DATABASE_ASYNC_URL=f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@db:{DB_PORT}/{DB_NAME}'

SCHEMA = os.getenv('SCHEMA')
SOURCE_API_URL = os.getenv('SOURCE_API_URL')