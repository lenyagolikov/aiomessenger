from http import HTTPStatus
from uuid import uuid4

from aiohttp import web
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from messenger.api.models import CreateChatModel
from messenger.db.models import Chat, Client
from messenger.logger import log_db_request
from messenger.utils.auth import cookie_storage, login_required
from messenger.utils.db import available_db
from messenger.utils import responses


@login_required
async def create_chat(request):
    """Валидирует поля, проверяет сессию с клиентом и создает чат"""
    chat = CreateChatModel.parse_raw(await request.text())
    async_session = request.app["db"]

    if not await available_db(async_session):
        return responses.db_not_available()

    session = await cookie_storage.load_session(request)
    client_login = session["login"]
    chat_id = await add_chat_to_db(async_session, chat.name, client_login)

    data = {"chat_id": chat_id}
    return web.json_response(data=data, status=HTTPStatus.CREATED)


@log_db_request
async def add_chat_to_db(async_session, chat_name, client_login):
    """Добавляет чат в БД и возвращает его ID"""
    async with async_session() as session:
        stmt = select(Client).options(selectinload(Client.chats))
        client = await session.execute(stmt.where(Client.login == client_login))
        client = client.scalar()

        chat = Chat(chat_id=str(uuid4()), chat_name=chat_name, client_id=client)
        client.chats.append(chat)

        session.add_all([chat, client])
        await session.commit()
    return chat.chat_id
