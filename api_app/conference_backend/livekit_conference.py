"""
Module for managing LiveKit conference operations.
"""
from api_app.schemas.conferences import ConferenceCreateModel, ConferenceModel, ConferenceOutputModel, ConferenceParticipantCreate, ConferenceParticipant
from api_app.schemas.errors import ErrorResponseModel
from api_app.datebases import conference_requests as db_requests
from api_app.settings import LIVEKIT_BACKEND


async def create_livekit_conference(conference: ConferenceCreateModel) -> ConferenceOutputModel | ErrorResponseModel:
    """
    Create a Jitsi conference.
    """
    
    conference_db = ConferenceModel(
        id=conference.id,
        speaker_id=conference.speaker_id,
        listeners=[ConferenceParticipantCreate(user_id=user_id) for user_id in conference.listeners],
        start_datetime=conference.start_datetime,
        end_datetime=conference.end_datetime,
        conference_link=f"{LIVEKIT_BACKEND["host"]}/{conference.id}",
        recording=conference.recording,
        is_ended=conference.is_ended
    )
    response: ConferenceModel | ErrorResponseModel = await db_requests.insert_conference(conference_db)
    if isinstance(response, ErrorResponseModel):
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
