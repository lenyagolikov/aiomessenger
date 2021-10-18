from http import HTTPStatus

from aiohttp import web
from sqlalchemy.future import select

from messenger.api.models import RegisterModel
from messenger.db.models import Client
from messenger.logger import log_db_request
from messenger.utils.db import available_db
from messenger.utils import responses


async def registration(request):
    """Валидирует поля, возвращает сообщение о статусе регистрации"""
    fields = RegisterModel.parse_raw(await request.text())
    async_session = request.app['db']

    if not await available_db(async_session):
        await responses.db_not_available()

    if not await add_client_to_db(async_session, fields.login, fields.password):
        data = {'message': 'Login already exists'}
        return web.json_response(data=data, status=HTTPStatus.CONFLICT)

    data = {'message': 'Registration is successful'}
    return web.json_response(data=data, status=HTTPStatus.CREATED)


@log_db_request
async def add_client_to_db(async_session, login, password):
    """Возвращает True, если логин не занят и клиент добавлен в БД. Иначе False"""
    async with async_session() as session:
        client = await session.execute(select(Client).where(Client.login == login))

        if client.scalar():
            return False

        new_client = Client(login=login, password=password)
        session.add(new_client)
        await session.commit()
    return True
