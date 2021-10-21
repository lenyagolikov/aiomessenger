from http import HTTPStatus

from aiohttp import web
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from messenger.api.models import GetMessagesModel
from messenger.db.models import Chat, User
from messenger.logger import log_db_request
from messenger.utils import responses
from messenger.utils.auth import cookie_storage, login_required
from messenger.utils.bot import redirect_to_bot
from messenger.utils.cache import mem_cache
from messenger.utils.db import available_db


@login_required
async def get_messages_from_chat(request):
    """
    Валидирует поля, проверяет сессию с клиентом, права доступа и возвращает сообщения
    """
    message = GetMessagesModel.parse_obj(request.query)
    async_session = request.app["db"]
    chat_id = request.match_info["chat_id"]

    session = await cookie_storage.load_session(request)
    client_login = session.get("login")

    if not await available_db(async_session):
        return await redirect_to_bot(async_session, chat_id)

    try:
        await permissions_for_read_messages(async_session, chat_id, client_login)
    except ValueError as err:
        return responses.resourse_not_found(err)

    from_ = int(message.from_)
    cursor = message.limit + from_ - 1

    messages = await get_messages_from_db(async_session, chat_id, from_, cursor)

    cursor = min(cursor, len(messages))

    data = {
        "messages": [{"text": msg.text} for msg in messages],
        "next": {"iterator": str(cursor + 1)},
    }
    return web.json_response(data=data, status=HTTPStatus.OK)


@mem_cache
@log_db_request
async def get_messages_from_db(async_session, chat_id, from_, cursor):
    """Возвращает сообщения из БД (декоратор - из кэша)"""
    async with async_session() as session:
        stmt = select(Chat).options(selectinload(Chat.messages))
        chat = await session.execute(stmt.where(Chat.chat_id == chat_id))
        chat = chat.scalar()
        messages = chat.messages
    return messages[from_ - 1 : cursor]


@log_db_request
async def permissions_for_read_messages(async_session, chat_id, client_login):
    """Проверяет права доступа клиента к пользователю и к чату"""
    async with async_session() as session:
        user = await session.execute(
            select(User)
            .where(User.client_id == client_login)
            .where(User.chat_id == chat_id)
        )

        user = user.scalar()

        if not user:
            raise ValueError("chat not found")
