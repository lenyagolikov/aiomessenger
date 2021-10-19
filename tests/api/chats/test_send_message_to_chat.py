import pytest


@pytest.mark.parametrize(
    "params, data",
    [
        ({"user_id": "user"}, {"message": "Hello"}),
        ({"user_id": "another-user"}, {"message": "Bye"}),
        ({"user_id": 135}, {"message": 135}),
        ({"user_id": 0}, {"message": 201}),
    ],
)
@pytest.mark.status_201
async def test_successful_send_message_to_chat(api_client, params, data):
    resp = await api_client.post(
        "/v1/chats/{chat_id}/messages", params=params, json=data
    )
    status_code = resp.status
    expected_status_code = 201
    assert (
        status_code == expected_status_code
    ), f"Expected status code {expected_status_code}, but taken {status_code}"


@pytest.mark.parametrize(
    "params, data",
    [
        ({"user_i": "user"}, {"message": "Hello"}),
        ({"user_id": "another-user"}, {"essage": "Bye"}),
        ({"user_id": 0}, {"message": [4, 5, 6]}),
    ],
)
@pytest.mark.status_400
async def test_bad_send_message_to_chat(api_client, params, data):
    resp = await api_client.post(
        "/v1/chats/{chat_id}/messages", params=params, json=data
    )
    status_code = resp.status
    expected_status_code = 400
    assert (
        status_code == expected_status_code
    ), f"Expected status code {expected_status_code}, but taken {status_code}"
