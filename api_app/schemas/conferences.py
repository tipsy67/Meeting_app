"""
Schemas for the Google Services application.
"""
import uuid
from datetime import datetime
from typing import Optional, Annotated
from pydantic import BaseModel, Field


class UserModel(BaseModel):
    """
    User schema representing a participant in the conference.
    This schema includes:
        id: int - telegram id
        first name: str (optional) - telegram first_name
        last name: str (optional) - telegram last_name
        username: str (optional) - telegram username
        is_speaker: bool - for set role speaker
        speaker_stream_key: - stream key if user is speaker

    * use alias _id only for searalization for MongoDB
    """
    id: Annotated[int, Field(serialization_alias="_id")]
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    is_speaker: bool = False



class StreamModel(BaseModel):
    """
    Model for Stream object
    """
    id: Annotated[str, Field(serialization_alias="_id")]
    user_id: int
    stream_key: str



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
    speaker_id: str
    users: list[int]
    speaker_id: str
    broadcast_id: str
    recording_url: str
    start_datetime: datetime
    end_datetime: datetime
    is_ended: bool = False
