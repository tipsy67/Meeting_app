"""
Module for managing Jitsi conference operations.
"""

from api_app.settings import JITSI_BACKEND
from api_app.schemas.conferences import (
    ConferenceCreateModel,
    ConferenceModel,
    ConferenceOutputModel,
    RecordingModel,
    ConferenceParticipant,
)
from api_app.schemas.errors import ErrorResponseModel
from api_app.datebases import conference_requests as db_requests
from api_app.datebases.conference_requests import get_stream_by_user_id
from google_services.youtube_api_utils import create_broadcast_async


async def create_jitsi_recording(
    conference: ConferenceModel,
) -> RecordingModel | ErrorResponseModel:
    """
    Create a Jitsi recording.
    """
    stream = await get_stream_by_user_id(conference.speaker_id)
    if not stream:
        return ErrorResponseModel(
            detail="Stream not found for the speaker", status_code=404
        )
    broadcast = await create_broadcast_async(
        title=f"broadcast for user#{conference.speaker_id}",
        start_datetime=conference.start_datetime,
        end_datetime=conference.start_datetime,
        stream_id=stream.id,
    )
    if not broadcast:
        return ErrorResponseModel(detail="Failed to create broadcast", status_code=500)
    recording_object = RecordingModel(
        conference_id=conference.id,
        recording_url=f"https://www.youtube.com/live/{broadcast}",
    )
    return recording_object


async def create_jitsi_conference(
    conference: ConferenceCreateModel,
) -> ConferenceOutputModel | ErrorResponseModel:
    """
    Create a Jitsi conference.
    """
    # create a Jitsi conference instance -> insert to db
    conference_db = ConferenceModel(
        id=conference.id,
        speaker_id=conference.speaker_id,
        listeners=[ConferenceParticipant(user_id) for user_id in conference.listeners],
        start_datetime=conference.start_datetime,
        end_datetime=conference.end_datetime,
        conference_link=f"{JITSI_BACKEND['host']}/{conference.id}",
        recording=conference.recording,
        is_ended=conference.is_ended,
    )
    response: ConferenceModel | ErrorResponseModel = (
        await db_requests.insert_conference(conference_db)
    )
    if isinstance(response, ErrorResponseModel):
        return response
    conference_output = ConferenceOutputModel(
        id=response.id,
        speaker_id=response.speaker_id,
        listeners=response.listeners,
        start_datetime=response.start_datetime,
        end_datetime=response.end_datetime,
        conference_link=response.conference_link,
    )
    if conference.recording:
        recording = await create_jitsi_recording(conference_db)
        if isinstance(recording, ErrorResponseModel):
            return recording
        conference_output.recording_url = recording.recording_url

    return conference_output
