from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from messenger.db.models import User
from messenger.db.storage_user_settings import users
from messenger.utils.db import available_db


async def get_user_settings(async_session, user_id):
    """Возвращает настройки пользователя из БД или из файла"""
    if await available_db(async_session):
        async with async_session() as session:
            stmt = select(User).options(selectinload(User.settings))
            user = await session.execute(stmt.where(User.id == user_id))
            user_settings = user.scalar().settings[0]
            return user_settings

    for user in users:
        if user.user_id == user_id:
            return user
