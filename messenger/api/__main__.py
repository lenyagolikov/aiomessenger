from aiohttp import web

from messenger.api.app import create_app


def main():
    app = create_app()
    web.run_app(app, port=8080, host='0.0.0.0')


if __name__ == '__main__':
    main()
