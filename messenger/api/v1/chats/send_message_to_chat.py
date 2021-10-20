from http import HTTPStatus

from aiohttp import web
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from messenger.api.models import SendMessageModel
from messenger.db.models import Chat, User, Message
from messenger.logger import log_db_request
from messenger.utils.auth import cookie_storage, login_required
from messenger.utils.cache import invalidate_cache
from messenger.utils.db import available_db
from messenger.utils import responses


@login_required
async def send_message_to_chat(request):
    """
    Валидирует поля, проверяет сессию с клиентом, возвращает статус отправки сообщения
    """
    body = await request.json()
    message = SendMessageModel(**request.query, **body)
    async_session = request.app["db"]

    if not await available_db(async_session):
        return responses.db_not_available()

    session = await cookie_storage.load_session(request)
    client_login = session["login"]
    chat_id = request.match_info["chat_id"]

    try:
        message_id = await add_message_to_db(
            async_session, chat_id, message.user, message.text, client_login
        )
    except ValueError as err:
        return responses.resourse_not_found(err)

    data = {"message_id": message_id}
    return web.json_response(data=data, status=HTTPStatus.CREATED)


@invalidate_cache
@log_db_request
async def add_message_to_db(async_session, chat_id, user_id, text, client_login):
    """
    Проверяет корректность данных и сохраняет сообщение в БД.
    Возвращает ID сообщения в чате
    """
    async with async_session() as session:
        stmt = select(User).options(selectinload(User.messages))
        user = await session.execute(stmt.where(User.user_id == user_id))
        user = user.scalar()

        if not user or user.client_id != client_login:
            raise ValueError("user not found")

        stmt = select(Chat).options(selectinload(Chat.messages))
        chat = await session.execute(stmt.where(Chat.chat_id == chat_id))
        chat = chat.scalar()

        if not chat or user.chat_id != chat_id:
            raise ValueError("chat not found")

        message = Message(text=text, user_id=user, chat_id=chat)

        chat.messages.append(message)
        user.messages.append(message)

        session.add(message)
        await session.commit()
    return len(chat.messages)
