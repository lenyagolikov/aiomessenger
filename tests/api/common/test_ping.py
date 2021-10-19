from http import HTTPStatus


async def test_ping(api_client):
    response = await api_client.get("/ping")
    assert response.status == HTTPStatus.OK

    body = await response.json()
    assert body["message"] == "app is working"
