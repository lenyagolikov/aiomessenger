from http import HTTPStatus

import pytest


@pytest.mark.parametrize(
    "fields",
    [
        {"user_name": "allison"},
        {"user_name": "allison 13", "лишнее поле": "лишнее поле"},
    ],
)
async def test_add_to_existing_chat(chat, api_client, fields):
    response = await api_client.post(f"/v1/chats/{chat}/users", json=fields)
    assert response.status == HTTPStatus.CREATED

    body = await response.json()
    assert "user_id" in body


@pytest.mark.parametrize(
    "fields",
    [
        {"user_name": "allison"},
        {"user_name": "allison 13", "лишнее поле": "лишнее поле"},
    ],
)
async def test_add_to_not_existing_chat(login, api_client, fields):
    response = await api_client.post("/v1/chats/bad_chat/users", json=fields)
    assert response.status == HTTPStatus.NOT_FOUND

    body = await response.json()
    assert "message" in body


@pytest.mark.parametrize(
    "fields",
    [
        {},
        {"user_name1": "new user"},
        {"user_name": ""},
        {"": "new-user"},
    ],
)
async def test_bad_params(chat, api_client, fields):
    response = await api_client.post(f"/v1/chats/{chat}/users", json=fields)
    assert response.status == HTTPStatus.BAD_REQUEST

    body = await response.json()
    assert "message" in body
