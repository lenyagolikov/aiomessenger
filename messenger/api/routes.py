from messenger.api.handlers.create_chat import create_chat
from messenger.api.handlers.add_user_to_chat import add_user_to_chat
from messenger.api.handlers.get_messages_from_chat import get_messages_from_chat
from messenger.api.handlers.send_message_to_chat import send_message_to_chat

from messenger.api.handlers.ping import ping_app
from messenger.api.handlers.ping_db import ping_db

from messenger.api.handlers.registration import registration
from messenger.api.handlers.login import login
from messenger.api.handlers.logout import logout


def setup_routes(app):
    app.router.add_get('/ping', ping_app)
    app.router.add_get('/ping_db', ping_db)

    app.router.add_post('/v1/chats', create_chat)
    app.router.add_post('/v1/chats/{chat_id}/users', add_user_to_chat)
    app.router.add_get('/v1/chats/{chat_id}/messages', get_messages_from_chat)
    app.router.add_post('/v1/chats/{chat_id}/messages', send_message_to_chat)

    app.router.add_post('/v1/auth/register', registration)
    app.router.add_post('/v1/auth/login', login)
    app.router.add_post('/v1/auth/logout', logout)
