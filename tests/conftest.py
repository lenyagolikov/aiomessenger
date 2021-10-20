import pytest

from sqlalchemy.ext.asyncio import create_async_engine

from messenger.api.app import create_app
from messenger.db.models import Base

DB_URL = "postgresql+asyncpg://lenyagolikov:1234@localhost/db_pytest"


@pytest.fixture
async def postgres():
    """
    Подготавливает тестовую БД и возвращает его URL
    """
    engine = create_async_engine(DB_URL)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    return DB_URL


@pytest.fixture
def bad_postgres():
    """
    Возвращает URL несуществующей БД
    """
    return DB_URL + "not found"


@pytest.fixture
async def api_client(aiohttp_client, postgres):
    """
    Создает тестовый экземпляр приложения для выполнения запросов
    """
    app = await create_app(postgres)
    client = await aiohttp_client(app)

    try:
        yield client
    finally:
        await client.close()
