from http import HTTPStatus

from aiohttp import web

from messenger.utils.auth import cookie_storage


async def logout(request):
    """Удаляет сессию из хранилища и куков, если они есть"""
    session = await cookie_storage.load_session(request)

    if session.empty:
        data = {'message': 'Already logout'}
        return web.json_response(data=data, status=HTTPStatus.BAD_REQUEST)

    session.invalidate()

    data = {'message': 'Logout is successful'}
    response = web.json_response(data=data, status=HTTPStatus.OK)

    await cookie_storage.save_session(request, response, session)

    return response
