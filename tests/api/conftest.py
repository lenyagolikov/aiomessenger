import pytest

from messenger.api.app import create_app


@pytest.fixture
async def api_client(aiohttp_client, postgres):
    """Создает клиента для приложения"""
    app = await create_app(postgres)
    client = await aiohttp_client(app)

    try:
        yield client
    finally:
        await client.close()


@pytest.fixture
async def api_client_without_db(aiohttp_client, bad_postgres):
    """Создает клиента для приложения"""
    app = await create_app(bad_postgres)
    client = await aiohttp_client(app)

    try:
        yield client
    finally:
        await client.close()
