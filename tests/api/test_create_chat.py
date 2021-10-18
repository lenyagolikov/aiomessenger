import pytest


@pytest.mark.parametrize('data', [{'chat_name': 'new chat'}, {'chat_name': 'новый чат'},
                                  {'chat_name': 'new-chat'}, {'chat_name': 'новый_чат'},
                                  {'chat_name': 'чатик', 'лишнее поле': 'лишнее поле'},
                                  {'chat_name': 'чатик', 'chat_name': 'чатик2'}]
                        )
@pytest.mark.status_201
async def test_successful_create_chat(api_client, data):
    resp = await api_client.post('/v1/chats', json=data)
    status_code = resp.status
    expected_status_code = 201
    assert status_code == expected_status_code,\
        f'Expected status code {expected_status_code}, but taken {status_code}'


@pytest.mark.parametrize('data', [{'chat_name1': 'new chat'}, {'chat_name': ''},
                                  {'': 'new-chat'}, {'chat-name': 'новый_чат'},
                                  {'новое поле': 'чатик', 'лишнее поле': 'лишнее поле'}, {}]
                        )        
@pytest.mark.status_400
async def test_bad_create_chat(api_client, data):
    resp = await api_client.post('/v1/chats', json=data)
    status_code = resp.status
    expected_status_code = 400
    assert status_code == expected_status_code,\
        f'Expected status code {expected_status_code}, but taken {status_code}'
