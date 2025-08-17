"""
Module for managing LiveKit conference operations.
"""

from api_app.datebases import conference_requests as db_requests
from api_app.schemas.conferences import (
    ConferenceCreateModel,
    ConferenceModel,
    ConferenceOutputModel,
    ConferenceParticipant,
    ConferenceParticipantCreate,
)
from api_app.schemas.errors import ErrorResponseModel
from api_app.settings import LIVEKIT_BACKEND


async def create_livekit_conference(
    conference: ConferenceCreateModel,
) -> ConferenceOutputModel | ErrorResponseModel:
    """
    Create a Jitsi conference.
    """
    listeners = [
        ConferenceParticipantCreate(user_id=user_id) for user_id in conference.listeners
    ]
    speaker = ConferenceParticipantCreate(user_id=conference.speaker)
    conference_db = ConferenceModel(
        id=conference.id,
        speaker=ConferenceParticipant(
            **ConferenceParticipantCreate.model_dump(speaker)
        ),
        lecture_name=conference.lecture_name,
        duration=conference.duration,
        listeners=[
            ConferenceParticipant(**ConferenceParticipantCreate.model_dump(user))
            for user in listeners
        ],
        start_datetime=conference.start_datetime,
        end_datetime=conference.end_datetime,
        conference_link=f"{LIVEKIT_BACKEND["host"]}/{conference.id}",
        recording=conference.recording,
        is_ended=conference.is_ended,
    )
    response: ConferenceModel | ErrorResponseModel = (
        await db_requests.insert_conference(conference_db)
    )
    return response
