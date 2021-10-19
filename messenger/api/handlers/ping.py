from http import HTTPStatus

from aiohttp import web


async def ping_app(request):
    """Возвращает сообщение о статусе работы приложения"""
    data = {"message": "app is working"}
    return web.json_response(data=data, status=HTTPStatus.OK)
