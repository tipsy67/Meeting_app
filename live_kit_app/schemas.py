"""
Module for schemas for LiveKit app
"""
from pydantic import BaseModel


class TelegramMessage(BaseModel):
    """
    Model for object which used for sending message to Telegram
    """
    conference_id: str
    text: str
    name: str | None = None
