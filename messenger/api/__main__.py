from aiohttp import web

from messenger.api.app import create_app
from messenger.utils.db import DB_URL


def main():
    app = create_app("postgresql+asyncpg" + DB_URL)
    web.run_app(app, port=8080, host="0.0.0.0")


if __name__ == "__main__":
    main()
