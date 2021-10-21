from http import HTTPStatus
from uuid import uuid4

from aiohttp import web
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from messenger.api.models import CreateTaskModel
from messenger.db.models import Client, User, Task
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


async def add_task_to_db(async_session, client_login):
    """
    Добавляет таску в БД и возвращает task id
    """
    async with async_session() as session:
        stmt = select(Client).options(selectinload(Client.tasks))
        client = await session.execute(stmt.where(Client.login == client_login))
        client = client.scalar()

        task = Task(task_id=str(uuid4()), client_id=client, status="WAITING")
        client.tasks.append(task)

        session.add_all([client, task])
        await session.commit()
    return task.task_id


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


@login_required
async def get_status_task(request):
    """
    Возвращает статус задачи
    """
    task_id = request.match_info["task_id"]
    async_session = request.app["db"]

    if not await available_db(async_session):
        return responses.db_not_available()

    session = await cookie_storage.load_session(request)
    client_login = session["login"]

    async with async_session() as session:
        task = await session.execute(select(Task).where(Task.task_id == task_id))
        task = task.scalar()

        if not task or task.client_id != client_login:
            return responses.resourse_not_found("task not found")

    data = {"status": task.status}
    return web.json_response(data=data, status=HTTPStatus.OK)


@login_required
async def get_messages(request):
    """
    Возвращает список сообщений из чатов
    """
    messages = ["Hello"]
    cursor = 1

    data = {
        "messages": [{"text": msg} for msg in messages],
        "next": {"iterator": str(cursor + 1)},
    }
    return web.json_response(data=data, status=HTTPStatus.OK)
