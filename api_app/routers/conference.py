
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from starlette import status

from api_app.datebases import conference_requests as db
from api_app.schemas.conferences import StreamModel, ConferenceModel, ConferenceCreateModel
from api_app.schemas.errors import ErrorResponseModel

router = APIRouter(prefix="/conferences", tags=["conferences"])


@router.post('/new')
async def create_conference_rt(conference: ConferenceCreateModel):
    """
    Create a new conference.
    """
    request = await db.insert_conference(
        speaker_id=conference.speaker_id,
        listeners=conference.listeners,
        start_datetime=conference.start_datetime,
        end_datetime=conference.end_datetime
    )
    if isinstance(request, ErrorResponseModel):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ErrorResponseModel.model_dump(request)
        )
    return request
