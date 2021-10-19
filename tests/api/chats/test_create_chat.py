from http import HTTPStatus

import pytest


@pytest.mark.parametrize(
    "fields",
    [
        {"chat_name": "new chat"},
        {"chat_name": "чатик", "лишнее поле": "лишнее поле"},
    ],
)
async def test_create_chat(login, api_client, fields):
    response = await api_client.post("/v1/chats", json=fields)
    assert response.status == HTTPStatus.CREATED

    body = await response.json()
    assert "chat_id" in body


@pytest.mark.parametrize(
    "fields",
    [
        {},
        {"chat_name1": "new chat"},
        {"chat_name": ""},
        {"": "new-chat"},
    ],
)
async def test_create_chat_bad_params(login, api_client, fields):
    response = await api_client.post("/v1/chats", json=fields)
    assert response.status == HTTPStatus.BAD_REQUEST

    body = await response.json()
    assert "message" in body


@pytest.mark.parametrize(
    "fields",
    [
        {"chat_name": "new chat"},
        {"chat_name": "новый чат"},
    ],
)
async def test_create_chat_without_auth(api_client, fields):
    response = await api_client.post("/v1/chats", json=fields)
    assert response.status == HTTPStatus.UNAUTHORIZED

    body = await response.json()
    assert "message" in body
