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
    """Создает чат для тестов, возвращает chat id"""
    fields = {"chat_name": "new_chat"}
    response = await api_client.post("/v1/chats", json=fields)
    body = await response.json()
    return body["chat_id"]


@pytest.fixture
async def new_user_in_chat(new_chat, api_client):
    """Создает юзера для тестов, возвращает chat id и user id"""
    fields = {"user_name": "new_user"}
    response = await api_client.post(f"/v1/chats/{new_chat}/users", json=fields)
    body = await response.json()
    return new_chat, body["user_id"]
