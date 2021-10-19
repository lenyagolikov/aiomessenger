from http import HTTPStatus

from sqlalchemy.ext.asyncio import create_async_engine


async def test_db_available(api_client):
    response = await api_client.get("/ping_db")
    assert response.status == HTTPStatus.OK

    body = await response.json()
    assert "message" in body


async def test_db_not_available(api_client, bad_postgres):
    engine = create_async_engine(bad_postgres)
    api_client.app["db"].configure(bind=engine)

    response = await api_client.get("/ping_db")
    assert response.status == HTTPStatus.SERVICE_UNAVAILABLE

    body = await response.json()
    assert "message" in body
