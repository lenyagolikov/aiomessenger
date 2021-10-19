from http import HTTPStatus

import pytest


@pytest.mark.parametrize(
    "params",
    [
        {"limit": 5},
        {"limit": 5, "from": 2},
    ],
)
async def test_get_from_existing_chat(chat_user, api_client, params):
    chat_id, _ = chat_user
    response = await api_client.get(f"/v1/chats/{chat_id}/messages", params=params)
    assert response.status == HTTPStatus.OK

    body = await response.json()
    assert "messages" in body and "next" in body


@pytest.mark.parametrize(
    "params",
    [
        {"limit": 5},
        {"limit": 5, "from": 2},
    ],
)
async def test_get_from_not_existing_chat(chat_user, api_client, params):
    response = await api_client.get("/v1/chats/bad_chat/messages", params=params)
    assert response.status == HTTPStatus.NOT_FOUND

    body = await response.json()
    assert "message" in body


@pytest.mark.parametrize(
    "params",
    [
        {},
        {"limit": -1},
        {"limit": 1001},
        {"limit": "string"},
        {"from": 5},
    ],
)
async def test_bad_params(chat_user, api_client, params):
    chat_id, _ = chat_user
    response = await api_client.get(f"/v1/chats/{chat_id}/messages", params=params)
    assert response.status == HTTPStatus.BAD_REQUEST

    body = await response.json()
    assert "message" in body
