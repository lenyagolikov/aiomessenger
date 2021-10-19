from http import HTTPStatus


async def test_app_available(api_client):
    response = await api_client.get("/ping")
    assert response.status == HTTPStatus.OK

    body = await response.json()
    assert "message" in body
