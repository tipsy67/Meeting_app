
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from starlette import status

from api_app.conference_backend import ConferenceBackend
from api_app.datebases.conference_requests import insert_conference, insert_recording
from api_app.schemas.conferences import ConferenceModel, ConferenceOutputModel, ConferenceCreateModel
from api_app.schemas.errors import ErrorResponseModel

from api_app.settings import CONFERENCE_BACKEND
router = APIRouter(prefix="/conferences", tags=["conferences"])


@router.post('/new')
async def create_conference_rt(conference: ConferenceCreateModel):
    """
    Create a new conference.
    """
    conference = ConferenceBackend.init(
        backend_name=CONFERENCE_BACKEND,
        conference=conference
    )

    if isinstance(conference, ErrorResponseModel):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ErrorResponseModel.model_dump(conference)
        )
    insert_to_db = await insert_conference(conference.details)
    if isinstance(insert_to_db, ErrorResponseModel):
        return JSONResponse(
            status_code=insert_to_db.status_code,
            content=ErrorResponseModel.model_dump(insert_to_db)
        )
    if insert_to_db.recording:
        recording = await conference.recording_details
        if isinstance(recording, ErrorResponseModel):
            return JSONResponse(
                status_code=recording.status_code,
                content=ErrorResponseModel.model_dump(recording)
            )
        recording_to_db = await insert_recording(recording)

        if isinstance(recording_to_db, ErrorResponseModel):
            return JSONResponse(
                status_code=recording_to_db.status_code,
                content=ErrorResponseModel.model_dump(recording_to_db)
            )
        conference_output = ConferenceOutputModel(
            **ConferenceModel.model_dump(insert_to_db),
            recording_url=recording_to_db.recording_url,
        )
        return conference_output

    else:
        conference_output = ConferenceOutputModel(
            id=insert_to_db.id,
            speaker_id=insert_to_db.speaker_id,
            listeners=insert_to_db.listeners,
            start_datetime=insert_to_db.start_datetime,
            end_datetime=insert_to_db.end_datetime,
            conference_link=insert_to_db.conference_link,
        )
    return ConferenceOutputModel.model_dump(conference_output)