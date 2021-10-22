import asyncio
from http import HTTPStatus
from uuid import uuid4

from aiohttp import web
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from messenger.api.models import CreateTaskModel, GetMessagesModel
from messenger.db.models import Client, Message, Task, User
from messenger.utils import responses
from messenger.utils.auth import login_required
from messenger.utils.auth import cookie_storage
from messenger.utils.db import available_db


@login_required
async def create_task(request):
    """
    Создает таску поиска сообщений в чатах, в которых состоит пользователь
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

    task_id = await add_task_to_db(async_session, client_login)

    asyncio.create_task(
        search_messages_in_chats(async_session, task_id, message.text, chats)
    )

    data = {"task_id": task_id}
    return web.json_response(data=data, status=HTTPStatus.CREATED)


async def add_task_to_db(async_session, client_login):
    """
    Добавляет таску в БД
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
        users = await session.execute(
            select(User).where(User.client_id == client_login)
        )
        users = users.scalars().all()

        if not users:
            raise ValueError("chats not found")

        chats = []

        for user in users:
            chats.append(user.chat_id)

    return chats


@login_required
async def get_status_task(request):
    """
    Возвращает статус таски
    """
    task_id = request.match_info["task_id"]
    async_session = request.app["db"]

    if not await available_db(async_session):
        return responses.db_not_available()

    session = await cookie_storage.load_session(request)
    client_login = session["login"]

    try:
        task = await get_task_from_db(async_session, task_id, client_login)
    except ValueError as err:
        return responses.resourse_not_found(err)

    data = {"status": task.status}
    return web.json_response(data=data, status=HTTPStatus.OK)


@login_required
async def get_result_task(request):
    """
    Возвращает результат таски
    """
    message = GetMessagesModel.parse_obj(request.query)
    async_session = request.app["db"]

    if not await available_db(async_session):
        return responses.db_not_available()

    session = await cookie_storage.load_session(request)
    client_login = session.get("login")
    task_id = request.match_info["task_id"]

    try:
        await get_task_from_db(async_session, task_id, client_login)
    except ValueError as err:
        return responses.resourse_not_found(err)

    from_ = int(message.from_)
    cursor = message.limit + from_ - 1

    messages = await get_messages_from_task(async_session, task_id, from_, cursor)

    cursor = min(cursor, len(messages))

    data = {
        "messages": [{"text": msg.text, "chat_id": msg.chat_id} for msg in messages],
        "next": {"iterator": str(cursor + 1)},
    }
    return web.json_response(data=data, status=HTTPStatus.OK)


async def get_task_from_db(async_session, task_id, client_login):
    """
    Возвращает таску из БД
    """
    async with async_session() as session:
        task = await session.execute(select(Task).where(Task.task_id == task_id))
        task = task.scalar()

        if not task or task.client_id != client_login:
            raise ValueError("task not found")

    return task


async def get_messages_from_task(async_session, task_id, from_, cursor):
    """
    Возвращает список сообщений из результата таски
    """
    async with async_session() as session:
        stmt = select(Task).options(selectinload(Task.messages))
        task = await session.execute(stmt.where(Task.task_id == task_id))
        task = task.scalar()
        messages = task.messages
    return messages[from_ - 1: cursor]


async def search_messages_in_chats(async_session, task_id, message, chats):
    """
    Процесс поиска сообщений в чатах для указанной таски
    """
    async with async_session() as session:
        await asyncio.sleep(5)  # чтобы следить статус таска для дебага
        stmt = select(Task).options(selectinload(Task.messages))
        task = await session.execute(stmt.where(Task.task_id == task_id))
        task = task.scalar()

        task.status = "IN PROCESS"
        session.add(task)
        await session.commit()

        messages = await session.execute(
            select(Message)
            .where(Message.text.ilike(f"%{message}%"), Message.chat_id.in_(chats))
            .limit(1000)
            .order_by(Message.date_created.desc())
        )
        messages = messages.scalars().all()
        task.messages.extend(messages)

        await asyncio.sleep(5)  # чтобы следить статус таска для дебага
        task.status = "SUCCESS"
        session.add(task)
        await session.commit()
        asyncio.create_task(clean_task_from_db(async_session, task_id))


async def clean_task_from_db(async_session, task_id):
    """
    Фоновым процессом чистит отработавший таск
    """
    await asyncio.sleep(60)

    async with async_session() as session:
        task = await session.execute(select(Task).where(Task.task_id == task_id))
        task = task.scalar()

        await session.delete(task)
        await session.commit()
