from http import HTTPStatus

import pytest


@pytest.mark.parametrize(
    "fields",
    [
        {"login": "allison", "password": "1234"},  # correct fields
    ],
)
async def test_login_successful(registration, api_client, fields):
    response = await api_client.post("/v1/auth/login", json=fields)
    assert response.status == HTTPStatus.OK

    body = await response.json()
    assert body["login"] == fields["login"]


@pytest.mark.parametrize(
    "fields",
    [
        {},  # empty fields
        {"password": "1234"},  # not login
        {"login": "NewUser"},  # not password
        {"login": "1", "password": "1234"},  # short login
        {"login": "NewUser1", "password": "1"},  # short password
        {"login": "", "password": ""},  # both empty,
    ],
)
async def test_login_bad_params(api_client, fields):
    response = await api_client.post("/v1/auth/login", json=fields)
    assert response.status == HTTPStatus.BAD_REQUEST

    body = await response.json()
    assert body["message"] == "bad-parameters"


@pytest.mark.parametrize(
    "fields",
    [
        {"login": "allison1", "password": "1234"},  # incorrect login
        {"login": "allison", "password": "12345"},  # incorrect password
        {"login": "lenyagolikov", "password": "lenyagolikov"},  # both incorrect
    ],
)
async def test_login_incorrect_fields(registration, api_client, fields):
    response = await api_client.post("/v1/auth/login", json=fields)
    assert response.status == HTTPStatus.UNAUTHORIZED

    body = await response.json()
    assert body["message"] == "Login or password is not correct"
