from datetime import datetime

from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)

Base = declarative_base()


class Client(Base):
    __tablename__ = "clients"

    id = Column(BigInteger, primary_key=True)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow)

    chats = relationship("Chat", backref="client")
    users = relationship("User", backref="client")

    def __repr__(self):
        return f"{{Client: {self.login}}}"


class Chat(Base):
    __tablename__ = "chats"

    id = Column(BigInteger, primary_key=True)
    chat_id = Column(String, unique=True, nullable=False)
    chat_name = Column(String, nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow)

    client_id = Column(ForeignKey("clients.login", ondelete="CASCADE"))

    users = relationship("User", backref="chat")
    messages = relationship("Message", backref="chat")

    def __repr__(self):
        return f"{{Chat: {self.chat_name}}}"


class User(Base):
    __tablename__ = "users"

    __table_args__ = (UniqueConstraint("user_id", "chat_id"),)

    id = Column(BigInteger, primary_key=True)
    user_id = Column(String, nullable=False)
    user_name = Column(String, nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow)

    chat_id = Column(ForeignKey("chats.chat_id", ondelete="CASCADE"))
    client_id = Column(ForeignKey("clients.login", ondelete="CASCADE"))

    messages = relationship("Message", backref="user")
    settings = relationship("UserSettings", backref="user")

    def __repr__(self):
        return f"{{User: {self.user_name}}}"


class Message(Base):
    __tablename__ = "messages"

    id = Column(BigInteger, primary_key=True)
    text = Column(String, nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow)

    chat_id = Column(ForeignKey("chats.chat_id", ondelete="CASCADE"))
    user_id = Column(ForeignKey("users.id", ondelete="SET NULL"))

    def __repr__(self):
        return f"{{Message: {self.text}}}"


class UserSettings(Base):
    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True)
    timezone = Column(Integer, nullable=False, default=0)

    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"))

    def __repr__(self):
        return f"{{timezone: {self.timezone}}}"
