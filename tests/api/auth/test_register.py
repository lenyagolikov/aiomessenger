from http import HTTPStatus

import pytest


@pytest.mark.parametrize('fields', [
    {'login': 'NewUser1', 'password': '1234'},
    {'login': 'NewUser2', 'password': '1234'},
    {'login': 'NewUser3', 'password': '12345'},
    {'login': 'NewUser4', 'password': '12345'},
])
async def test_register_successful(api_client, fields):
    response = await api_client.post('/v1/auth/register', json=fields)
    assert response.status == HTTPStatus.CREATED


@pytest.mark.parametrize('fields', [
    {},  # empty fields
    {'password': '1234'},  # not login
    {'login': 'NewUser'},  # not password
    {'login': '1', 'password': '1234'},  # short login
    {'login': 'NewUser1', 'password': '1'},  # short password
    {'login': '', 'password': ''}  # empty login and empty password,
])
async def test_register_bad_params(api_client, fields):
    response = await api_client.post('/v1/auth/register', json=fields)
    assert response.status == HTTPStatus.BAD_REQUEST


async def test_register_client_already_exists(api_client):
    fields = {'login': 'allison', 'password': '1234'}
    await api_client.post('/v1/auth/register', json=fields)
    response = await api_client.post('/v1/auth/register', json=fields)
    assert response.status == HTTPStatus.CONFLICT