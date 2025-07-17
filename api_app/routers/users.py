
from fastapi import APIRouter
from starlette import status

from api_app.datebases import users_requests as db
from api_app.schemas.users import SpeakerListener, UserCreateUpdate, LectureRequest

router = APIRouter(prefix="/users", tags=["users"])


@router.post('', status_code=status.HTTP_200_OK)
async def set_user_rt(tg_user: UserCreateUpdate):
    return await db.set_user(tg_user)


@router.get('/speakers', status_code=status.HTTP_200_OK)
async def get_all_speakers_rt():
    return await db.get_all_speakers()


@router.post('/speakers/listeners', status_code=status.HTTP_200_OK)
async def add_listener_to_speaker_rt(data: SpeakerListener):
    return await db.add_listener_to_speaker(data)


@router.get('/listeners', status_code=status.HTTP_200_OK)
async def get_listeners_rt(speaker_id: int):
    return await db.get_listeners(speaker_id)


@router.get('/listeners/speakers', status_code=status.HTTP_200_OK)
async def get_speakers_for_listener_rt(listener_id:int):
    return await db.get_speakers(listener_id)

@router.delete('/listeners/speakers', status_code=status.HTTP_200_OK)
async def remove_from_listeners_rt(listener_id:int, speaker_id:int):
    return await db.delete_listener_from_speaker(listener_id, speaker_id)


