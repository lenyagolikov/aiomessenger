import pytest


@pytest.mark.parametrize('data', [{'user_name': 'new user13'}, {'user_name': 'новый юзер'},
                                  {'user_name': 'new-user2'}, {'user_name': 'новый_юзер'},
                                  {'user_name': 'юзер3', 'лишнее поле': 'лишнее поле'},
                                  {'user_name': 'юзер2', 'user_name': 'юзер4'}]
                         )
@pytest.mark.status_201
async def test_successful_add_user_to_chat(api_client, data):
    resp = await api_client.post('/v1/chats/{chat_id}/users', json=data)
    status_code = resp.status
    expected_status_code = 201
    assert status_code == expected_status_code,\
        f'Expected status code {expected_status_code}, but taken {status_code}'


@pytest.mark.parametrize('data', [{'user_name1': 'new user'}, {'user_name': ''},
                                  {'': 'new-user'}, {'user-name': 'новый_юзер'},
                                  {'новое поле': 'юзер', 'лишнее поле': 'лишнее поле'}, {}]
                         )
@pytest.mark.status_400
async def test_bad_add_user_to_chat(api_client, data):
    resp = await api_client.post('/v1/chats/{chat_id}/users', json=data)
    status_code = resp.status
    expected_status_code = 400
    assert status_code == expected_status_code,\
        f'Expected status code {expected_status_code}, but taken {status_code}'
