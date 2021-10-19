import os
from pathlib import Path

from alembic.config import Config
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

from messenger.logger import log_db_request

POSTGRES_USER = os.getenv("POSTGRES_USER", "lenyagolikov")
POSTGRES_PWD = os.getenv("POSTGRES_PWD", "1234")
POSTGRES_HOST = os.getenv("POSTGRES_HOSTS", "localhost").split(",")[-1]
POSTGRES_DB = os.getenv("POSTGRES_DB", "messenger")

DB_URL = f'://{POSTGRES_USER}:{POSTGRES_PWD}@{POSTGRES_HOST}/{POSTGRES_DB}'

PROJECT_PATH = Path(__file__).parent.parent.resolve()


@log_db_request
async def available_db(async_session):
    """Возвращает True, если есть подключение к БД. Иначе False"""
    async with async_session() as session:
        try:
            await session.execute(text("select 1"))
        except Exception:
            return False
        return True


def make_alembic_config(cmd_opts, base_path=PROJECT_PATH) -> Config:
    """
    Создает объект конфигурации alembic на основе аргументов командной строки,
    подменяет относительные пути на абсолютные.
    """
    # Подменяем путь до файла alembic.ini на абсолютный
    if not os.path.isabs(cmd_opts.config):
        cmd_opts.config = os.path.join(base_path, cmd_opts.config)

    config = Config(file_=cmd_opts.config, ini_section=cmd_opts.name,
                    cmd_opts=cmd_opts)

    # Подменяем путь до папки с alembic на абсолютный
    alembic_location = config.get_main_option('script_location')
    if not os.path.isabs(alembic_location):
        config.set_main_option('script_location',
                               os.path.join(base_path, alembic_location))
    if cmd_opts.db_url:
        config.set_main_option('sqlalchemy.url', cmd_opts.db_url)

    return config


async def setup_db(app, db_url):
    engine = create_async_engine(db_url)
    
    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession)

    app['db'] = async_session

    try:
        yield
    finally:
        await engine.dispose()
