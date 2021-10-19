import pytest


@pytest.mark.parametrize(
    "params",
    [
        {"limit": 1, "from": "ok"},
        {"limit": "1", "from": "test"},
        {"limit": 1000, "from": "test-driver"},
        {"limit": "1000", "from": "da_da_da"},
        {"limit": 50, "from": "hello world"},
        {"limit": "100", "from": "friend"},
        {"limit": 500},
        {"limit": "100"},
        {"limit": 100},
    ],
)
@pytest.mark.status_201
async def test_successful_get_messages_from_chat(api_client, params):
    resp = await api_client.get("/v1/chats/{chat_id}/messages", params=params)
    status_code = resp.status
    expected_status_code = 200
    assert (
        status_code == expected_status_code
    ), f"Expected status code {expected_status_code}, but taken {status_code}"


@pytest.mark.parametrize(
    "params",
    [
        {"limit": -1},
        {"from": "onlyfrom"},
        {"limit": 0},
        {"limit": 1001},
        {"limit": "1001"},
        {"limit": "0"},
        {"limit": -5},
        {"limit": -500},
    ],
)
@pytest.mark.status_400
async def test_bad_get_messages_from_chat(api_client, params):
    resp = await api_client.get("/v1/chats/{chat_id}/messages", params=params)
    status_code = resp.status
    expected_status_code = 400
    assert (
        status_code == expected_status_code
    ), f"Expected status code {expected_status_code}, but taken {status_code}"
