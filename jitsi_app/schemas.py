"""
Schemas for the Jitsi application.
"""
from datetime import datetime
from typing import Optional, Annotated
import uuid
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
    speaker_stream_key: Optional[str] = None


class LectureHallModel(BaseModel):
    """
    LectureHall schema representing a group of users
    who are members of lection by speaker.
    This schema includes:
        name: str - title of group/lecture
        description: str (optional) - description of group/lecture
        speaker_id: int - id of user who owner of the group/lecture
        listenerd: list[int] - list of users id who listening the lecture
    """
    name: str
    description: Optional[str] = None
    speaker_id: int
    listeners: Optional[list[int]] = []


class ConferenceModel(BaseModel):
    """
    Conference schema representing a conference session.
        id: str - uuid id (for generate uniq link)
        lecture_hall_id: str - for wich group or lecture
        recording_link: str - link for stream and recording video (broadcast_id)
        start_datetime: datetim for start conference
        end_datetime: datetime for end conference
    """
    id: Annotated[
        str,
        Field(
            default_factory=lambda: str(uuid.uuid4()),
            serialization_alias="_id"
        )
    ]
    lecture_hall_id: int
    recording_link: str
    start_datetime: datetime
    end_time: datetime
