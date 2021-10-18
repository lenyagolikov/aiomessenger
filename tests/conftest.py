import os
from types import SimpleNamespace

import pytest
from sqlalchemy_utils import create_database, drop_database
from yarl import URL

from messenger.utils.db import DB_URL, make_alembic_config

DB_URL = os.getenv('CI_MESSENGER_DB_URL', 'postgresql' + DB_URL)


@pytest.fixture
def postgres():
    """Создает временную БД для запуска теста"""
    db_name = 'db_pytest'
    db_url = str(URL(DB_URL).with_path(db_name))
    create_database(db_url)

    try:
        yield db_url
    finally:
        drop_database(db_url)


@pytest.fixture()
def alembic_config(postgres):
    """Создает объект с конфигурацией для alembic, настроенный на временную БД"""
    cmd_options = SimpleNamespace(config='alembic.ini', name='alembic',
                                  db_url=postgres, raiseerr=False, x=None)
    return make_alembic_config(cmd_options)
