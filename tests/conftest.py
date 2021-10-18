import sys

import pytest

sys.path.append('/home/lenyagolikov/code/yandex/messenger/')
sys.path.append('/home/lenyagolikov/code/yandex/messenger/messenger/api')

from messenger.api import create_app


@pytest.fixture
async def api_client(aiohttp_client):
    app = create_app()
    client = await aiohttp_client(app)

    try:
        yield client
    finally:
        await client.close()
