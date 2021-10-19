from http import HTTPStatus

from aiohttp import web
from aiohttp_session import new_session
from sqlalchemy.future import select

from messenger.api.models import LoginModel
from messenger.db.models import Client
from messenger.logger import log_db_request
from messenger.utils.auth import cookie_storage
from messenger.utils.db import available_db
from messenger.utils import responses


async def login(request):
    """
    Валидирует поля, сохраняет сессию с клиентом в случае успешной аутентификации
    """
    fields = LoginModel.parse_raw(await request.text())
    async_session = request.app["db"]

    if not await available_db(async_session):
        await responses.db_not_available()

    if not await correct_login_and_password(
        async_session, fields.login, fields.password
    ):
        data = {"message": "Login or password is not correct"}
        return web.json_response(data=data, status=HTTPStatus.UNAUTHORIZED)

    data = {"login": fields.login}
    response = web.json_response(data=data, status=HTTPStatus.OK)

    await save_client_session_id(request, response, fields.login)

    return response


@log_db_request
async def correct_login_and_password(async_session, login, password):
    """Возвращает True, если логин и пароль правильные. Иначе False"""
    async with async_session() as session:
        client = await session.execute(select(Client).where(Client.login == login))
        client = client.scalar()

        if not client:
            return False

        if client.login != login or client.password != password:
            return False

    return True


async def save_client_session_id(request, response, login):
    """Сохраняет сессию в хранилище и в куках"""
    session = await new_session(request)
    session["login"] = login
    await cookie_storage.save_session(request, response, session)
