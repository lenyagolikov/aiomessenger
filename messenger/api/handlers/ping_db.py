from http import HTTPStatus

from aiohttp import web

from messenger.utils.db import available_db


async def ping_db(request):
    """Возвращает сообщение о статусе подключения к БД"""
    async_session = request.app['db']
    available = await available_db(async_session)

    if not available:
        data = {'message': 'DB is not available'}
        return web.json_response(data=data, status=HTTPStatus.SERVICE_UNAVAILABLE)

    data = {'message': 'DB is available'}
    return web.json_response(data=data, status=HTTPStatus.OK)
