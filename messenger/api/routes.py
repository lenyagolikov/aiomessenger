from messenger.api.common.ping_app import ping_app
from messenger.api.common.ping_db import ping_db

from messenger.api.v1.auth.registration import registration
from messenger.api.v1.auth.login import login
from messenger.api.v1.auth.logout import logout

from messenger.api.v1.chats.create_chat import create_chat
from messenger.api.v1.chats.add_user_to_chat import add_user_to_chat
from messenger.api.v1.chats.get_messages_from_chat import get_messages_from_chat
from messenger.api.v1.chats.send_message_to_chat import send_message_to_chat


def setup_routes(app):
    app.router.add_get("/ping", ping_app)
    app.router.add_get("/ping_db", ping_db)

    app.router.add_post("/v1/chats", create_chat)
    app.router.add_post("/v1/chats/{chat_id}/users", add_user_to_chat)
    app.router.add_get("/v1/chats/{chat_id}/messages", get_messages_from_chat)
    app.router.add_post("/v1/chats/{chat_id}/messages", send_message_to_chat)

    app.router.add_post("/v1/auth/register", registration)
    app.router.add_post("/v1/auth/login", login)
    app.router.add_post("/v1/auth/logout", logout)
