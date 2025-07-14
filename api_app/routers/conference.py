
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from starlette import status

from api_app.conference_backend.conference import create_conference
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
    conference_output = await create_conference(CONFERENCE_BACKEND, conference)
    return conference_output
