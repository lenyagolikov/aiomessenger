from http import HTTPStatus

from aiohttp import web

from messenger.utils.db import available_db
from messenger.utils import responses


async def ping_db(request):
    """Возвращает сообщение о статусе подключения к БД"""
    async_session = request.app["db"]

    if not await available_db(async_session):
        return await responses.db_not_available()

    data = {"message": "DB is available"}
    return web.json_response(data=data, status=HTTPStatus.OK)
