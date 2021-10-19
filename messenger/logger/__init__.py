from decimal import Decimal

import logging.config
import time

from .settings import LOGGER_CONFIG

logging.config.dictConfig(LOGGER_CONFIG)

log = logging.getLogger("log")


def execution_time(start_time):
    """Возвращает время выполнения кода в миллисекундах"""
    result = time.time() - start_time
    result = round(Decimal(result), 3)
    return result


def log_request(handler):
    """Записывает в логи информацию об клиентском запросе и серверном ответе"""

    async def inner(*args, **kwargs):
        start_time = time.time()
        request = args[0]

        response = await handler(*args, **kwargs)

        execution_time = time.time() - start_time
        execution_time = round(Decimal(execution_time), 3)

        log.debug(
            f"{execution_time} ms - {request.method} [{response.status}]: {request.url}"
        )

        return response

    return inner


def log_db_request(handler):
    """Записывает в логи информацию о запросе в БД"""

    async def inner(*args, **kwargs):
        handler_name = handler.__name__
        start_time = time.time()

        try:
            response = await handler(*args, **kwargs)
        except ValueError as err:
            result = execution_time(start_time)
            log.error(f'{result} ms - "{handler_name}" - {err}')
            raise ValueError
        else:
            result = execution_time(start_time)
            log.debug(f'{result} ms - DB_SESSION: "{handler_name}" - {response}')
            return response

    return inner
