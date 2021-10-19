from http import HTTPStatus

from aiohttp import web

from .user_settings import get_user_settings


async def redirect_to_bot(async_session, user_id):
    """Перенаправляет пользователя к системному боту-пользователю"""
    greetings = {
        1: "Доброе утро",
        2: "Добрый день",
        3: "Добрый вечер",
        4: "Доброй ночи",
        "default": "Здравствуйте",
    }

    settings = await get_user_settings(async_session, user_id)

    try:
        greeting = greetings[settings.timezone]
    except AttributeError:
        greeting = greetings["default"]

    data = {
        "messages": [
            {"text": f"{greeting}, {user_id}, система находится в процессе подъёма"}
        ],
        "next": {"iterator": "bot-message"},
    }
    return web.json_response(data=data, status=HTTPStatus.OK)
