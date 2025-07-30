"""
Schemas for the Google Services application.
"""

import uuid
from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, Field

# Models for conference management


class ConferenceCreateModel(BaseModel):
    """
    Base Model for Meeting Conference
    *speakers & listeners are user IDs
    """

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    speaker: int
    lecture_name: str = "undefined"
    listeners: list[int] = list
    start_datetime: datetime
    duration: int = 40
    end_datetime: datetime = datetime.min
    recording: bool = False
    is_ended: bool = False


class ConferenceParticipantCreate(BaseModel):
    """
    Model for convert user_id to Participant object
    With token for conference auth

    *id - auto generate token for auth at conference
        send link to conference with parametr:
        http://conference_url/<conference_id>?<participant_id>
    """

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: int


class ConferenceParticipant(ConferenceParticipantCreate):
    """
    Model of Participant for db & output
    """

    id: str = Field(serialization_alias="_id")


class ConferenceParticipantOutput(ConferenceParticipant):
    """
    Model of Participant for db & output
    """

    id: str = Field(validation_alias="_id")


class ConferenceModel(ConferenceCreateModel):
    """
    Base Model for Meeting Conference
    *speakers & listeners are user IDs
    """

    id: str = Field(serialization_alias="_id")
    conference_link: str
    recording_url: str | None = None
    speaker: ConferenceParticipant
    listeners: list[ConferenceParticipant]


class ConferenceOutputModel(ConferenceModel):
    """
    Base Model for Meeting Conference
    Output data for routers
    *speakers & listeners are user IDs
    """

    id: str = Field(validation_alias="_id")
    speaker: ConferenceParticipantOutput
    listeners: list[ConferenceParticipantOutput]


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
