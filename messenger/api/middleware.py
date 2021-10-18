from http import HTTPStatus

from aiohttp import web
from aiohttp.web_exceptions import HTTPMethodNotAllowed, HTTPNotFound, HTTPServerError
from aiohttp.web_middlewares import middleware
from pydantic import ValidationError

from messenger.logger import log_request


@middleware
@log_request
async def error_middleware(request, handler):

    try:
        return await handler(request)
    except ValidationError as err:
        data = {'message': 'bad-parameters'}
        status = HTTPStatus.BAD_REQUEST
    except HTTPNotFound as err:
        data = {'message': err.reason}
        status = HTTPStatus.NOT_FOUND
    except HTTPMethodNotAllowed as err:
        data = {'message': err.reason}
        status = HTTPStatus.METHOD_NOT_ALLOWED
    except HTTPServerError as err:
        data = {'message': err.reason}
        status = err.status_code
    except Exception:
        data = {'message': 'Internal Server Error'}
        status = HTTPStatus.INTERNAL_SERVER_ERROR

    return web.json_response(data=data, status=status)
