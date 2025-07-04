"""
Schemas for the Jitsi application.
"""
import datetime
from pydantic import BaseModel, Field
from typing import Optional
import uuid


def generate_uuid():
    """
    Generation UUID
    """
    return str(uuid.uuid1())


class User(BaseModel):
    """
    User schema representing a participant in the conference.
    This schema includes the user's Telegram ID, first name, last name, and username.
    It is used to identify users in the conference system.
    _id = telegram id
    """
    id: str = Field(..., alias="_id")
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None


class Speaker(BaseModel):
    """
    Speaker schema representing a speaker in the conference.
    This schema includes the speaker's ID and the user information.
    It is used to identify speakers in the conference system.
    """
    user_id: str

    class Config:
        orm_mode = True

class SpeakerInDB(Speaker):
    id: str = Field(default_factory=generate_uuid, alias="_id")


class SpeakerOut(BaseModel):
    id: str
    user: User

    class Config:
        orm_mode = True


class CreateLecture(BaseModel):
    """
    Lecture schema representing a lecture in the conference.
    This schema includes the lecture's ID, name, speaker information,
    a list of listeners (users), and the stream key and URL.
    It is used to manage the lecture details in the conference system.
    """
    id: str = Field(default_factory=generate_uuid(), alias="_id")
    name: str
    speaker_id: str
    listener_ids: Optional[list[str]]
    stream_key: str
    stream_url: Optional[str] = None

    class Config:
        orm_mode = True


class Lecture(BaseModel):
    """
    Lecture schema representing a lecture in the conference.
    This schema includes the lecture's ID, name, speaker information,
    a list of listeners (users), and the stream key and URL.
    It is used to manage the lecture details in the conference system.
    """
    id: str
    name: str
    speaker: Speaker
    listeners: Optional[list[User]]
    stream_key: str
    stream_url: Optional[str] = None

    class Config:
        orm_mode = True


class CreateConference(BaseModel):
    """
    Conference schema representing a conference session.
    This schema includes the conference's ID, lecture information,
    the URL for the conference, and the start time.
    It is used to manage the conference session details in the system.
    """
    id: str = Field(default_factory=generate_uuid(), alias="_id")
    lecture_id: str
    url: str
    start_time: str

    class Config:
        orm_mode = True


class Conference(BaseModel):
    """
    Conference schema representing a conference session.
    This schema includes the conference's ID, lecture information,
    the URL for the conference, and the start time.
    It is used to manage the conference session details in the system.
    """
    id: str
    lecture: Lecture
    url: str
    start_time: datetime.datetime

    class Config:
        orm_mode = True
