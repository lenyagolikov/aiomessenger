from http import HTTPStatus

from aiohttp import web


async def db_not_available():
    data = {"message": "DB is not available"}
    return web.json_response(data=data, status=HTTPStatus.SERVICE_UNAVAILABLE)


async def resourse_not_found(message):
    data = {"message": message}
    return web.json_response(data=data, status=HTTPStatus.NOT_FOUND)
