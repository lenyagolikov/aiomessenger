import pytest

from alembic.command import upgrade
from sqlalchemy import create_engine

from messenger.api.app import create_app


@pytest.fixture
async def migrated_postgres(alembic_config, postgres):
    """Возвращает URL к БД с примененными миграциями"""
    upgrade(alembic_config, 'head')
    return postgres


@pytest.fixture
async def api_client(aiohttp_client):
    """Создает клиента для приложения"""
    app = create_app()
    client = await aiohttp_client(app)

    try:
        yield client
    finally:
        await client.close()


@pytest.fixture
def migrated_postgres_connection(migrated_postgres):
    """Соединяется синхронно с БД"""
    engine = create_engine(migrated_postgres)
    conn = engine.connect()

    try:
        yield conn
    finally:
        conn.close()
        engine.dispose()
