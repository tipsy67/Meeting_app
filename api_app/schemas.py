from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel
from typing_extensions import Optional


class UserCreateUpdate(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str


class UserResponse(UserCreateUpdate):
    created_at: datetime
    last_activity: datetime
    is_active: bool
    is_admin: Optional[bool] = None
    is_speaker: Optional[bool] = None
    is_banned: Optional[str] = None


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
