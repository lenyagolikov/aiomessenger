from http import HTTPStatus


async def test_ping_db_available(api_client):
    response = await api_client.get("/ping_db")
    assert response.status == HTTPStatus.OK

    body = await response.json()
    assert body["message"] == "DB is available"


async def test_ping_db_not_available(api_client_without_db):
    response = await api_client_without_db.get("/ping_db")
    assert response.status == HTTPStatus.SERVICE_UNAVAILABLE

    body = await response.json()
    assert body["message"] == "DB is not available"
