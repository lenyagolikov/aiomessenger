import pytest
from sqlalchemy.ext.asyncio import create_async_engine

from messenger.db.models import Base

DB_URL = "postgresql+asyncpg://lenyagolikov:1234@localhost/db_pytest"


@pytest.fixture
async def postgres():
    """Подготавливает тестовую БД"""
    engine = create_async_engine(DB_URL)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    try:
        yield DB_URL
    finally:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await engine.dispose()
