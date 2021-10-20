from http import HTTPStatus

from aiohttp import web


def db_not_available():
    data = {"message": "DB is not available"}
    return web.json_response(data=data, status=HTTPStatus.SERVICE_UNAVAILABLE)


def resourse_not_found(message):
    data = {"message": str(message)}
    return web.json_response(data=data, status=HTTPStatus.NOT_FOUND)
