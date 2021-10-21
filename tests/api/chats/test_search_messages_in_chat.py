from http import HTTPStatus

import pytest


@pytest.mark.parametrize(
    "fields",
    [
        {"message": "allison"},
    ],
)
async def test_create_task_with_chats(chat_user, api_client, fields):
    response = await api_client.post("/v1/chats/search", json=fields)
    assert response.status == HTTPStatus.CREATED

    body = await response.json()
    assert "task_id" in body


@pytest.mark.parametrize(
    "fields",
    [
        {"message": "allison"},
    ],
)
async def test_create_task_without_chats(chat, api_client, fields):
    response = await api_client.post("/v1/chats/search", json=fields)
    assert response.status == HTTPStatus.NOT_FOUND

    body = await response.json()
    assert "message" in body


async def test_get_status_exist_task(task, api_client):
    response = await api_client.get(f"/v1/chats/search/status/{task}")
    assert response.status == HTTPStatus.OK

    body = await response.json()
    assert "status" in body


async def test_get_status_not_exist_task(task, api_client):
    response = await api_client.get(f"/v1/chats/search/status/bad_task")
    assert response.status == HTTPStatus.NOT_FOUND

    body = await response.json()
    assert "message" in body


@pytest.mark.parametrize(
    "params",
    [
        {"limit": 5},
        {"limit": 5, "from": 2},
    ],
)
async def test_get_result_exist_task(task, api_client, params):
    response = await api_client.get(f"/v1/chats/search/{task}/messages", params=params)
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
async def test_get_result_not_exist_task(task, api_client, params):
    response = await api_client.get(f"/v1/chats/search/bad_task/messages", params=params)
    assert response.status == HTTPStatus.NOT_FOUND

    body = await response.json()
    assert "message" in body
