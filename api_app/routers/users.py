from fastapi import APIRouter
from starlette import status

from api_app.datebases.mongo_requests import (
    add_listener_to_speaker,
    get_speakers,
    set_user, get_listeners,
)
from api_app.schemas import SpeakerListener, UserCreateUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.get('/speakers', status_code=status.HTTP_200_OK)
async def get_all_speakers():
    return await get_speakers()


@router.post('/add-to-speaker', status_code=status.HTTP_200_OK)
async def add_to_speaker(data: SpeakerListener):
    return await add_listener_to_speaker(data)


@router.get('/listeners', status_code=status.HTTP_200_OK)
async def get_speaker_listeners(speaker_id: int):
    return await get_listeners(speaker_id)


@router.post('', status_code=status.HTTP_200_OK)
async def create_user(tg_user: UserCreateUpdate):
    return await set_user(tg_user)


@router.put('')
async def update_user():
    pass


@router.delete('')
async def delete_user():
    pass
