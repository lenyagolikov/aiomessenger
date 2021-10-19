import base64
import os
from http import HTTPStatus

from aiohttp import web
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from cryptography import fernet

FERNET_KEY = fernet.Fernet.generate_key()
SECRET_KEY = base64.urlsafe_b64decode(FERNET_KEY)

cookie_storage = EncryptedCookieStorage(
    secret_key=SECRET_KEY, cookie_name="session_id", httponly=True
)

AUTH_DISABLED = os.getenv("AUTH_DISABLED", False)


def login_required(handler):
    """Возвращает 401, если клиент не прошел аутентификацию"""

    async def inner(request):
        if AUTH_DISABLED:
            return await handler(request)

        session = await cookie_storage.load_session(request)

        if session.empty:
            data = {"message": "login required"}
            return web.json_response(data=data, status=HTTPStatus.UNAUTHORIZED)

        return await handler(request)

    return inner
