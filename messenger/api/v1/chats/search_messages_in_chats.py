from http import HTTPStatus

from aiohttp import web
from sqlalchemy.future import select

from messenger.api.models import CreateTaskModel
from messenger.db.models import User
from messenger.utils import responses
from messenger.utils.auth import login_required
from messenger.utils.auth import cookie_storage
from messenger.utils.db import available_db


@login_required
async def create_task(request):
    """
    Запускает процесс поиска сообщений в чатах, в которых состоит пользователь
    """
    message = CreateTaskModel.parse_raw(await request.text())
    async_session = request.app["db"]

    if not await available_db(async_session):
        return responses.db_not_available()

    session = await cookie_storage.load_session(request)
    client_login = session["login"]

    try:
        chats = await get_client_chats(async_session, client_login)
    except ValueError as err:
        return responses.resourse_not_found(err)

    task_id = await add_task_to_db()
    
    data = {"task_id": task_id}
    return web.json_response(data=data, status=HTTPStatus.CREATED)


async def add_task_to_db():
    """
    Добавляет таску в БД и возвращает task id
    """



async def get_client_chats(async_session, client_login):
    """
    Возвращает список чатов, в которых состоит пользователь
    """
    async with async_session() as session:
        users = await session.execute(select(User).where(User.client_id == client_login))
        users = users.scalars()

        if not users:
            raise ValueError("chats not found")

        chats = []

        for user in users:
            chats.append(user.chat_id)

    return chats


async def get_status_task():
    """
    Возвращает статус задачи
    """
    pass


async def get_messages():
    """
    Возвращает список сообщений из чатов
    """
    pass
