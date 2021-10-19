from http import HTTPStatus

import pytest


@pytest.mark.parametrize(
    "fields",
    [
        {"login": "allison", "password": "1234"},
    ],
)
async def test_successful(register, api_client, fields):
    response = await api_client.post("/v1/auth/login", json=fields)
    assert response.status == HTTPStatus.OK

    body = await response.json()
    assert body["login"] == fields["login"]


@pytest.mark.parametrize(
    "fields",
    [
        {},
        {"password": "1234"},
        {"login": "NewUser"},
        {"login": "1", "password": "1234"},
        {"login": "NewUser1", "password": "1"},
        {"login": "", "password": ""},
    ],
)
async def test_bad_params(api_client, fields):
    response = await api_client.post("/v1/auth/login", json=fields)
    assert response.status == HTTPStatus.BAD_REQUEST

    body = await response.json()
    assert "message" in body


@pytest.mark.parametrize(
    "fields",
    [
        {"login": "allison1", "password": "1234"},
        {"login": "allison", "password": "12345"},
        {"login": "lenyagolikov", "password": "lenyagolikov"},
    ],
)
async def test_incorrect_login_and_password(register, api_client, fields):
    response = await api_client.post("/v1/auth/login", json=fields)
    assert response.status == HTTPStatus.UNAUTHORIZED

    body = await response.json()
    assert "message" in body
