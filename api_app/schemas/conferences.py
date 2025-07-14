"""
Schemas for the Google Services application.
"""
import uuid
from datetime import datetime
from typing import Optional, Annotated
from pydantic import BaseModel, Field

# Models for conference management

class ConferenceCreateModel(BaseModel):
    """
    Base Model for Meeting Conference
    *speakers & listeners are user IDs
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), serialization_alias="_id")
    speaker_id: int
    listeners: list[int]
    start_datetime: datetime
    end_datetime: datetime
    recording: bool = False
    is_ended: bool = False


class ConferenceModel(ConferenceCreateModel):
    """
    Base Model for Meeting Conference
    *speakers & listeners are user IDs
    """
    conference_link: str

class ConferenceOutputModel(ConferenceModel):
    """
    Base Model for Meeting Conference
    Output data for routers
    *speakers & listeners are user IDs
    """
    recording_url: str = None


# Models for recording management

class RecordingModel(BaseModel):
    """
    Base Model for Recording object
    """
    conference_id: str
    recording_url: str


class YoutubeStreamModel(BaseModel):
    """
    Model for Stream object
    For YouTube Live Streaming
    For conference which cant be recorded,
    But can be streamed to YouTube

    * Need save this model to database,
    because we need to link it with user for future reuse
    """
    id: Annotated[str, Field(alias="_id")]
    user_id: int
    stream_key: str


class YoutubeBroadcastModel(BaseModel):
    """
    Model for YouTube Broadcast object
    For conference which cant be recorded,
    But can be streamed to YouTube
    """
    id: str
    title: str
    start_datetime: datetime
    end_datetime: datetime
    stream_id: str
    recording_url: Optional[str] = None
