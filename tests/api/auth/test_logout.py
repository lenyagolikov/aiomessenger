from http import HTTPStatus


async def test_successful(login, api_client):
    response = await api_client.post("/v1/auth/logout")
    assert response.status == HTTPStatus.OK

    body = await response.json()
    assert body["login"] == login


async def test_already_logout(logout, api_client):
    response = await api_client.post("/v1/auth/logout")
    assert response.status == HTTPStatus.OK

    body = await response.json()
    assert "message" in body
