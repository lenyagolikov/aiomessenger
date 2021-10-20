from types import SimpleNamespace

import pytest
from alembic.command import downgrade, upgrade
from alembic.script import ScriptDirectory

from messenger.utils.db import make_alembic_config


def get_revisions():
    """
    Возвращает список ревизий
    """
    # Создаем объект с конфигурацей alembic (db_url не нужен)
    options = SimpleNamespace(
        config="alembic.ini", db_url=None, name="alembic", raiseerr=False, x=None
    )
    config = make_alembic_config(options)

    # Получаем директорию с миграциями alembic
    revisions_dir = ScriptDirectory.from_config(config)

    # Получаем миграции и сортируем в порядке от первой до последней
    revisions = list(revisions_dir.walk_revisions("base", "heads"))
    revisions.reverse()
    return revisions


@pytest.mark.parametrize("revision", get_revisions())
def test_migrations_stairway(alembic_config, revision):
    upgrade(alembic_config, revision.revision)
    # -1 используется для downgrade первой миграции (т.к. ее down_revision
    # равен None)
    downgrade(alembic_config, revision.down_revision or "-1")
    upgrade(alembic_config, revision.revision)
