from fastapi import APIRouter
from starlette import status

from api_app.datebases import mongo_requests
from api_app.schemas import SpeakerListener, UserCreateUpdate, LectureRequest

router = APIRouter(prefix="/users", tags=["users"])


@router.get('/speakers', status_code=status.HTTP_200_OK)
async def get_all_speakers_rt():
    return await mongo_requests.get_all_speakers()

@router.post('/save-lecture', status_code=status.HTTP_200_OK)
async def save_lecture_rt(data: LectureRequest):
    return await mongo_requests.save_lecture(data)

@router.post('/add-to-speaker', status_code=status.HTTP_200_OK)
async def add_listener_to_speaker_rt(data: SpeakerListener):
    return await mongo_requests.add_listener_to_speaker(data)


@router.get('/listeners', status_code=status.HTTP_200_OK)
async def get_listeners_rt(speaker_id: int):
    return await mongo_requests.get_listeners(speaker_id)


@router.post('', status_code=status.HTTP_200_OK)
async def set_user_rt(tg_user: UserCreateUpdate):
    return await mongo_requests.set_user(tg_user)


@router.put('')
async def update_user():
    pass


@router.delete('')
async def delete_user():
    pass
