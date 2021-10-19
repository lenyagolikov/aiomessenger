import pytest


@pytest.fixture
async def registration(api_client):
    """Регистрирует клиента в приложении и возвращает логин и пароль"""
    fields = {"login": "allison", "password": "1234"}
    await api_client.post("/v1/auth/register", json=fields)
    return fields


@pytest.fixture
async def login(registration, api_client):
    """Авторизует клиента в приложении и возвращает логин, полученный из ответа"""
    response = await api_client.post("/v1/auth/login", json=registration)
    body = await response.json()
    return body["login"]


@pytest.fixture
async def logout(login, api_client):
    """Удаляет сессию с клиентом и возвращает его логин"""
    response = await api_client.post("/v1/auth/logout")
    body = await response.json()
    return body["login"]


@pytest.fixture
async def new_chat(login, api_client):
    """Создает чат для тестов и возвращает его ID"""
    fields = {"chat_name": "new_chat"}
    response = await api_client.post("/v1/chats", json=fields)
    body = await response.json()
    return body["chat_id"]
