from types import SimpleNamespace

import pytest
from sqlalchemy_utils import create_database, drop_database

from messenger.utils.db import make_alembic_config

DB_URL = 'postgresql://lenyagolikov:1234@localhost/migrations'


@pytest.fixture
def clean_postgres():
    """
    Создает временную БД для миграций и удаляет ее после
    """
    create_database(DB_URL)

    try:
        yield
    finally:
        drop_database(DB_URL)


@pytest.fixture()
def alembic_config(clean_postgres):
    """
    Создает объект с конфигурацией для alembic, настроенный на временную БД.
    """
    cmd_options = SimpleNamespace(config='alembic.ini', name='alembic',
                                  db_url=DB_URL, raiseerr=False, x=None)
    return make_alembic_config(cmd_options)
