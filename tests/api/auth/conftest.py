from http import HTTPStatus

import pytest


@pytest.fixture
async def register_client(api_client):
    """Регистрация клиента для тестов логина и логаута"""
    fields = {'login': 'allison', 'password': '1234'}
    response = await api_client.post('/v1/auth/register', json=fields)
    assert response.status == HTTPStatus.CREATED
