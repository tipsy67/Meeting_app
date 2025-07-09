"""
Schemas for the Google Services application.
"""
import uuid
from datetime import datetime
from typing import Optional, Annotated
from pydantic import BaseModel, Field



class StreamModel(BaseModel):
    """
    Model for Stream object
    """
    id: Annotated[str, Field(alias="_id")]
    user_id: int
    stream_key: str


class BroadcastModel(BaseModel):
    """
    Model for YouTube Broadcast object
    """
    id: str
    title: str
    start_datetime: datetime
    end_datetime: datetime
    stream_id: str
    recording_url: Optional[str] = None



class ConferenceModel(BaseModel):
    """
    Model for Jitsi Conference
    Link for user:
        https://host_conference/<conference_id>?token=<user_token>
    """
    id: Annotated[
        str,
        Field(
            default_factory=lambda: str(uuid.uuid4()),
            serialization_alias="_id"
        )
    ]
    speaker_id: int
    users: list[int]
    broadcast_id: str
    stream_key: str
    recording_url: str
    start_datetime: datetime
    end_datetime: datetime
    is_ended: bool = False


class ConferenceCreateModel(BaseModel):
    """
    Model for creating a conference
    """
    speaker_id: int
    listeners: list[int]
    start_datetime: datetime
    end_datetime: datetime
