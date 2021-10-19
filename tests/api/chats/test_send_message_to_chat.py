from http import HTTPStatus

import pytest


@pytest.mark.parametrize(
    "fields",
    [
        {"message": "Hello"},
        {"message": "Hello again"},
    ],
)
async def test_send_message_to_existing_chat(
        new_user_in_chat, api_client, fields):
    chat_id, user_id = new_user_in_chat
    params = {"user_id": user_id}
    response = await api_client.post(
        f"/v1/chats/{chat_id}/messages", params=params, json=fields
    )
    assert response.status == HTTPStatus.CREATED

    body = await response.json()
    assert "message_id" in body


@pytest.mark.parametrize(
    "fields",
    [
        {"message": "Hello"},
        {"message": "Hello again"},
    ],
)
async def test_send_message_to_not_existing_chat(
        new_user_in_chat, api_client, fields):
    _, user_id = new_user_in_chat
    params = {"user_id": user_id}
    response = await api_client.post(
        "/v1/chats/bad_chat/messages", params=params, json=fields
    )
    assert response.status == HTTPStatus.NOT_FOUND

    body = await response.json()
    assert "message" in body


@pytest.mark.parametrize(
    "fields",
    [
        {"": "Hello"},
        {"message": ""},
    ],
)
async def test_send_message_to_chat_bad_params(
        new_user_in_chat, api_client, fields):
    chat_id, user_id = new_user_in_chat
    params = {"user_id": user_id}
    response = await api_client.post(
        f"/v1/chats/{chat_id}/messages", params=params, json=fields
    )
    assert response.status == HTTPStatus.BAD_REQUEST

    body = await response.json()
    assert "message" in body
