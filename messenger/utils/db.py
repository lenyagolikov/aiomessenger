import os

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from messenger.logger import log_db_request

POSTGRES_USER = os.getenv("POSTGRES_USER", "lenyagolikov")
POSTGRES_PWD = os.getenv("POSTGRES_PWD", "1234")
POSTGRES_HOST = os.getenv("POSTGRES_HOSTS", "localhost").split(",")[-1]
POSTGRES_DB = os.getenv("POSTGRES_DB", "messenger")

DB_URL = f'://{POSTGRES_USER}:{POSTGRES_PWD}@{POSTGRES_HOST}/{POSTGRES_DB}'

engine = create_async_engine('postgresql+asyncpg' + DB_URL)

async_session = sessionmaker(
    engine,
    expire_on_commit=False,
    future=True,
    class_=AsyncSession
)


@log_db_request
async def available_db():
    """Возвращает True, если есть подключение к БД. Иначе False"""
    async with async_session() as session:
        try:
            await session.execute(text("select 1"))
        except Exception:
            return False
        return True
