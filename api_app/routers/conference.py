
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from starlette import status

from api_app.conference_backend.conference import create_conference
from api_app.datebases.conference_requests import get_conference
from api_app.schemas.conferences import ConferenceModel, ConferenceOutputModel, ConferenceCreateModel
from api_app.schemas.errors import ErrorResponseModel

from api_app.settings import CONFERENCE_BACKEND

#TODO: temporary import -> delete after rafactoring
from api_app.datebases.config_base import users_collection

router = APIRouter(prefix="/conferences", tags=["conferences"])


@router.post('/new')
async def create_conference_rt(conference: ConferenceCreateModel):
    """
    Create a new conference.
    """
    conference_output = await create_conference(CONFERENCE_BACKEND, conference)
    return conference_output.model_dump()


@router.get('/{conference_id}')
async def conference_detail_rt(conference_id: str):
    """
    Get detail of conference
    """
    conference = await get_conference(conference_id)
    if isinstance(conference, ErrorResponseModel):
        return JSONResponse(
            content={"error": conference.detail},
            status_code=conference.status_code
        )
    return conference.model_dump()


#TODO: temporary route, please ask developer of users routers to add this route
# !!! Need to request detail info about user (for send data to LiveKit App frontend) !!! #
@router.get("/get_user_detail/{user_id}")
async def get_user_by_id_rt(user_id: int):
    """
    User detail by user_id
    !!! Temporary Route !!!
    """
    user = await users_collection.find_one({"_id": user_id})
    user["id"] = user.pop("_id")
    return user
