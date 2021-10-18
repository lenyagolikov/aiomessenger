from aiohttp import web
from aiohttp_session import session_middleware

from messenger.api.middleware import error_middleware
from messenger.api.routes import setup_routes
from messenger.utils.auth import cookie_storage
from messenger.utils.db import async_session


async def create_app():
    app = web.Application(
        middlewares=[session_middleware(cookie_storage), error_middleware])
    setup_routes(app)
    app.on_startup.append(on_start)
    app.on_cleanup.append(on_shutdown)
    return app


async def on_start(app):
    app['db'] = async_session


async def on_shutdown(app):
    app['db'].close_all()
