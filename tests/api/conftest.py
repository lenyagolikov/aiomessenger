import pytest


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
