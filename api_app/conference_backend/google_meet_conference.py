"""
Module for managing Google Meet conference operations.
"""

from api_app.schemas.conferences import (ConferenceCreateModel,
                                         ConferenceModel,
                                         ConferenceOutputModel,
                                         ConferenceParticipant)
from api_app.schemas.errors import ErrorResponseModel
from google_services.calendar_api_utils import create_event


async def create_goole_meet_conference(
    conference: ConferenceCreateModel,
) -> ConferenceOutputModel | ErrorResponseModel:
    """
    Create a Jitsi conference.
    """
    event = await create_event(
        summary=f"Conference {conference.id}",
        start_time=conference.start_datetime.isoformat(),
        end_time=conference.end_datetime.isoformat(),
    )
    if not event:
        return ErrorResponseModel(
            status_code=500, detail="Failed to create Google Meet event"
        )
    conference_db = ConferenceModel(
        id=conference.id,
        speaker_id=conference.speaker_id,
        listeners=[ConferenceParticipant(user_id) for user_id in conference.listeners],
        start_datetime=conference.start_datetime,
        end_datetime=conference.end_datetime,
        conference_link=event,
        recording=conference.recording,
        is_ended=conference.is_ended,
    )
    if isinstance(conference_db, ErrorResponseModel):
        return conference_db
    conference_output = ConferenceOutputModel(
        id=conference_db.id,
        speaker_id=conference_db.speaker_id,
        listeners=conference_db.listeners,
        start_datetime=conference_db.start_datetime,
        end_datetime=conference_db.end_datetime,
        conference_link=conference_db.conference_link,
    )
    return conference_output
