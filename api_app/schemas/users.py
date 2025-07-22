from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, validator, field_validator, Field
from typing_extensions import Optional


class UserCreateUpdate(BaseModel):
    id: int
    username: Optional[str] = None
    first_name: str
    last_name: Optional[str] = None


class UserResponse(UserCreateUpdate):
    id: int = Field(alias="_id", serialization_alias="id")
    created_at: datetime
    last_activity: datetime
    is_active: bool
    is_admin: bool = False
    is_speaker: bool = False
    is_banned: bool = False


class SpeakerListener(BaseModel):
    speaker_id: int
    listener_id: int


class SpeakerListenerResponse(SpeakerListener):
    created_at: datetime

    class Config:
        json_encoders = {ObjectId: str}


class LectureRequest(BaseModel):
    name: str
    data: list[int]
