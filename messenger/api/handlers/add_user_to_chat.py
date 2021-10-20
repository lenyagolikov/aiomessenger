from http import HTTPStatus
from uuid import uuid4

from aiohttp import web
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from messenger.api.models import AddUserModel
from messenger.db.models import Chat, Client, User
from messenger.logger import log_db_request
from messenger.utils.auth import cookie_storage, login_required
from messenger.utils.db import available_db
from messenger.utils import responses


@login_required
async def add_user_to_chat(request):
    """
    Валидирует поля, проверяет сессию клиента и возвращает сообщение о статусе запроса
    """
    user = AddUserModel.parse_raw(await request.text())
    async_session = request.app["db"]

    if not await available_db(async_session):
        return responses.db_not_available()

    session = await cookie_storage.load_session(request)
    client_login = session["login"]
    chat_id = request.match_info["chat_id"]

    try:
        user_id = await add_user_to_db(async_session, chat_id, user.name, client_login)
    except ValueError as err:
        return responses.resourse_not_found(err)

    data = {"user_id": user_id}
    return web.json_response(data=data, status=HTTPStatus.CREATED)


@log_db_request
async def add_user_to_db(async_session, chat_id, user_name, client_login):
    """
    Добавляет пользователя в БД и возвращает его ID.
    Выбрасывает ValueError, если чата нет
    """
    async with async_session() as session:
        stmt = select(Chat).options(selectinload(Chat.users))
        chat = await session.execute(stmt.where(Chat.chat_id == chat_id))
        chat = chat.scalar()

        if not chat:
            raise ValueError("chat not found")

        stmt = select(Client).options(selectinload(Client.users))
        client = await session.execute(stmt.where(Client.login == client_login))
        client = client.scalar()

        user = User(
            user_id=str(uuid4()), user_name=user_name, chat_id=chat, client_id=client
        )

        chat.users.append(user)
        client.users.append(user)

        session.add_all([chat, client, user])
        await session.commit()
    return user.user_id
