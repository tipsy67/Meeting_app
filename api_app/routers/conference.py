import datetime

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from starlette import status

import api_app.services.conferences as srv
from api_app.conference_backend.conference import create_conference
from api_app.datebases.conference_requests import get_conference
from api_app.datebases.users_requests import get_listeners_ids_from_lecture
from api_app.schemas.conferences import ConferenceCreateModel
from api_app.schemas.errors import ErrorResponseModel
from api_app.settings import CONFERENCE_BACKEND

router = APIRouter(prefix="/conferences", tags=["conferences"])


@router.post("/new")
async def create_conference_rt(conference: ConferenceCreateModel):
    """
    Create a new conference.
    """
    conference.end_datetime = conference.start_datetime + datetime.timedelta(
        minutes=conference.duration
    )
    listeners = await get_listeners_ids_from_lecture(
        conference.speaker, conference.lecture_name
    )
    conference.listeners = listeners["listeners"]
    conference_output = await create_conference(CONFERENCE_BACKEND, conference)
    await srv.create_conference(conference_output.id)

    return conference_output.model_dump()


@router.get("/{conference_id}")
async def conference_detail_rt(conference_id: str):
    """
    Get detail of conference
    """
    conference = await get_conference(conference_id)
    if isinstance(conference, ErrorResponseModel):
        return JSONResponse(
            content={"error": conference.detail}, status_code=conference.status_code
        )
    return conference.model_dump()
