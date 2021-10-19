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
async def test_successful_get_messages_from_chat(user_in_chat, api_client, params):
    chat_id, user_id = user_in_chat
    response = await api_client.get(f"/v1/chats/{chat_id}/messages", params=params)
