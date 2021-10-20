import pytest

from alembic.command import upgrade

from messenger.api.app import create_app


@pytest.fixture
def migrated_postgres(alembic_config, postgres):
    """
    Возвращает URL к БД с примененными миграциями
    """
    upgrade(alembic_config, "head")
    return postgres


@pytest.fixture
async def api_client(aiohttp_client, migrated_postgres):
    """
    Создает тестовый экземпляр приложения для выполнения запросов
    """
    app = await create_app(migrated_postgres)
    client = await aiohttp_client(app)

    try:
        yield client
    finally:
        await client.close()


@pytest.fixture
async def register(api_client):
    """
    Регистрирует клиента в приложении и возвращает его логин и пароль
    """
    fields = {"login": "allison", "password": "1234"}
    await api_client.post("/v1/auth/register", json=fields)
    return fields


@pytest.fixture
async def login(register, api_client):
    """
    Авторизует клиента в приложении и его возвращает логин
    """
    response = await api_client.post("/v1/auth/login", json=register)
    body = await response.json()
    return body["login"]


@pytest.fixture
async def logout(login, api_client):
    """
    Удаляет сессию с клиентом и возвращает его логин
    """
    response = await api_client.post("/v1/auth/logout")
    body = await response.json()
    return body["login"]
