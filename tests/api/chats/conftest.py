import pytest


@pytest.fixture
async def chat(login, api_client):
    """
    Создает чат для тестов, возвращает chat id
    """
    fields = {"chat_name": "new_chat"}
    response = await api_client.post("/v1/chats", json=fields)
    body = await response.json()
    return body["chat_id"]


@pytest.fixture
async def chat_user(chat, api_client):
    """
    Создает юзера в чате для тестов, возвращает chat id и user id
    """
    fields = {"user_name": "new_user"}
    response = await api_client.post(f"/v1/chats/{chat}/users", json=fields)
    body = await response.json()
    return chat, body["user_id"]


@pytest.fixture
async def task(chat_user, api_client):
    """
    Создает таску для тестов и возвращает task id
    """
    fields = {"message": "allison"}
    response = await api_client.post(f"/v1/chats/search", json=fields)
    body = await response.json()
    return body["task_id"]
