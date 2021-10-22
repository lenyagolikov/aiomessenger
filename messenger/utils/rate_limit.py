import asyncio
import time

from messenger.utils.auth import cookie_storage


class RateLimiter:
    """
    Паттерн корзины с токенами
    У клиента 10 токенов - они расходуются после каждого запроса
    Чтобы не ограничить возможности добросовестного клиента, токены восстанавливаются,
    в зависимости от времени последнего запроса
    """
    RATE = 1
    MAX_TOKENS = 10

    def __init__(self, client):
        self.client = client
        self.tokens = self.MAX_TOKENS
        self.updated_at = time.monotonic()

    async def make_request(self):
        await self.wait_for_token()

    async def wait_for_token(self):
        while self.tokens < 1:
            self.add_new_tokens()
            await asyncio.sleep(0.1)
        self.tokens -= 1

    def add_new_tokens(self):
        now = time.monotonic()
        time_since_update = now - self.updated_at
        new_tokens = time_since_update * self.RATE
        self.tokens = min(self.tokens + new_tokens, self.MAX_TOKENS)
        self.updated_at = now


clients = {}


def rate_limit(handler):
    """
    Ограничивает количество запросов в секунду
    """
    async def inner(*args, **kwargs):
        request = args[0]

        session = await cookie_storage.load_session(request)
        client_login = session["login"]

        if client_login not in clients:
            client = RateLimiter(client_login)
            clients[client_login] = client
        else:
            await clients[client_login].make_request()

        return await handler(*args, **kwargs)
    return inner
