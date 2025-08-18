from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field, field_validator, validator
from typing_extensions import Optional

from api_app.core.config import settings


class UserCreateUpdate(BaseModel):
    id: int
    username: Optional[str] = None
    first_name: str
    last_name: Optional[str] = None
    language_code: Optional[str] = settings.default_language_code
    model_config = ConfigDict(extra="ignore")


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

    model_config = ConfigDict(json_encoders={ObjectId: str})


class UserToListResponse(BaseModel):
    id: int = Field(alias="_id", serialization_alias="id")
    username: str
    full_name: Optional[str] = None


class SpeakersListResponse(BaseModel):
    speakers: list[UserToListResponse]


class ListenersListResponse(BaseModel):
    listeners: list[UserToListResponse]


class ListenersFromLectureResponse(BaseModel):
    listeners: list[UserResponse]


class LectureRequest(BaseModel):
    name: str
    data: list[int]


class LectureResponse(BaseModel):
    lecture_name: str
    speaker_id: int
    listeners: list[int]
    updated_at: datetime

    model_config = ConfigDict(json_encoders={datetime: lambda v: v.isoformat()})


class LecturesBase(BaseModel):
    id: int
    name: str
    updated_at: datetime
    speaker: dict | None = None


class LecturesListResponse(BaseModel):
    lectures: list[LecturesBase]


class DeleteLectureResponse(BaseModel):
    deleted: LectureResponse
