from functools import partial

from aiohttp.web_app import Application
from aiohttp_session import session_middleware

from messenger.api.middleware import error_middleware
from messenger.api.routes import setup_routes
from messenger.utils.auth import cookie_storage
from messenger.utils.db import setup_db


async def create_app(db_url):
    """Создает экземпляр приложения"""
    app = Application(
        middlewares=[session_middleware(cookie_storage), error_middleware]
    )

    setup_routes(app)

    app.cleanup_ctx.append(partial(setup_db, db_url=db_url))

    return app
