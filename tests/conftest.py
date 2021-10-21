from types import SimpleNamespace
from uuid import uuid4

import asyncpg
import pytest
from yarl import URL

from messenger.utils.db import MESSENGER_DB_URL, make_alembic_config


@pytest.fixture
async def postgres(loop):
    """
    Создает временную БД для запуска теста
    """
    db_name = uuid4().hex
    db_user = "lenyagolikov"
    db_url = str(URL(MESSENGER_DB_URL).with_path(db_name))

    conn = await asyncpg.connect(
        database="template1", user="postgres", password="1234", host="localhost"
    )
    await conn.execute(f'CREATE DATABASE "{db_name}" OWNER "{db_user}"')

    try:
        yield db_url
    finally:
        await conn.execute(f'DROP DATABASE "{db_name}"')
        await conn.close()


@pytest.fixture
def bad_postgres():
    """
    Возвращает URL к несуществующей БД
    """
    return MESSENGER_DB_URL + "not found"


@pytest.fixture
def alembic_config(postgres):
    """
    Создает объект с конфигурацией для alembic, настроенный на временную БД.
    """
    cmd_options = SimpleNamespace(
        config="alembic.ini", name="alembic", db_url=postgres, raiseerr=False, x=None
    )
    return make_alembic_config(cmd_options)
