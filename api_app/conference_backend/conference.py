"""
Module with factories for manageing different conference backends.
"""

from typing import Dict, Callable
from api_app.schemas.conferences import (
    ConferenceCreateModel,
    ConferenceModel,
    ConferenceOutputModel,
    RecordingModel,
)
from api_app.schemas.errors import ErrorResponseModel
from api_app.conference_backend.jitsi_conference import create_jitsi_conference
from api_app.conference_backend.google_meet_conference import (
    create_goole_meet_conference,
)
from api_app.conference_backend.livekit_conference import create_livekit_conference


conference_creators: Dict[str, Callable] = {
    "google_meet": create_goole_meet_conference,
    "jitsi": create_jitsi_conference,
    "livekit": create_livekit_conference,
}


async def create_conference(
    backends, conference: ConferenceCreateModel
) -> ConferenceOutputModel | ErrorResponseModel:
    """
    Create a conference using the specified backend.
    """
    if backends not in conference_creators:
        return ErrorResponseModel(
            status_code=400, detail=f"Unsupported backend: {backends}"
        )
    return await conference_creators[backends](conference)
