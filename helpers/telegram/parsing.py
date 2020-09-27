from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class Chat(BaseModel):
    id_: int
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    title: Optional[str]
    type_: str

    class Config:
        fields = {
            'id_': 'id',
            'type_': 'type'
        }


class MessageFrom(BaseModel):
    id_: int
    is_bot: bool
    first_name: str
    last_name: Optional[str]
    username: str
    language_code: Optional[str]

    class Config:
        fields = {
            'id_': 'id'
        }


class Result(BaseModel):
    message_id: int
    from_: Optional[MessageFrom]
    chat: Chat
    date: datetime
    text: str

    class Config:
        fields = {
            'from_': 'from'
        }


class SendMessageResponse(BaseModel):
    ok: bool
    result: Result


class ChannelPost(BaseModel):
    id_: int
    chat: Chat
    date: datetime
    new_chat_title: Optional[str]
    text: Optional[str]

    class Config:
        fields = {
            'id_': 'id'
        }


class Message(BaseModel):
    message_id: int
    from_: MessageFrom
    chat: Chat
    date: datetime
    edit_date: Optional[datetime]
    text: Optional[str]
    reply_to_message: Optional['Message']
    sticker: Optional[dict]

    class Config:
        fields = {
            'from_': 'from'
        }


class GetUpdatesResult(BaseModel):
    update_id: int
    message: Optional[Message]
    channel_post: Optional[ChannelPost]
    edited_message: Optional[Message]


class GetUpdatesResponse(BaseModel):
    ok: bool
    result: List[GetUpdatesResult]
