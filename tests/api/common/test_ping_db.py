from http import HTTPStatus


async def test_db_available(api_client):
    response = await api_client.get("/ping_db")
    assert response.status == HTTPStatus.OK

    body = await response.json()
    assert "message" in body


async def test_db_not_available(api_client_without_db):
    response = await api_client_without_db.get("/ping_db")
    assert response.status == HTTPStatus.SERVICE_UNAVAILABLE

    body = await response.json()
    assert "message" in body
