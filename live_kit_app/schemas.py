"""
Module for schemas for LiveKit app
"""
from pydantic import BaseModel


class TelegramMessage(BaseModel):
    """
    Model for object which used for sending message to Telegram
    """
    chat_id: int
    text: str
