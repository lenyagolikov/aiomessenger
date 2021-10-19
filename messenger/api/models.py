from pydantic import BaseModel, Field


class CreateChatModel(BaseModel):
    name: str = Field(alias="chat_name", min_length=1, max_length=255)


class AddUserModel(BaseModel):
    name: str = Field(alias="user_name", min_length=1, max_length=255)


class SendMessageModel(BaseModel):
    text: str = Field(alias="message", min_length=1)
    user: str = Field(alias="user_id")


class GetMessagesModel(BaseModel):
    limit: int = Field(ge=1, le=1000)
    from_: str = Field(alias="from", default="1")


class RegisterModel(BaseModel):
    login: str = Field(min_length=2, max_length=255)
    password: str = Field(min_length=4, max_length=255)


class LoginModel(BaseModel):
    login: str = Field(min_length=2, max_length=255)
    password: str = Field(min_length=4, max_length=255)
