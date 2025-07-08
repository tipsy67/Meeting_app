
from fastapi import APIRouter
from starlette import status

from api_app.datebases import users_requests as db
from api_app.schemas.users import SpeakerListener, UserCreateUpdate, LectureRequest

router = APIRouter(prefix="/users", tags=["users"])


@router.get('/speakers', status_code=status.HTTP_200_OK)
async def get_all_speakers_rt():
    return await db.get_all_speakers()

@router.get('/speakers-selected', status_code=status.HTTP_200_OK)
async def get_speakers_rt(listener_id:int):
    return await db.get_speakers(listener_id)

@router.delete('/remove-from-listeners', status_code=status.HTTP_200_OK)
async def remove_from_listeners_rt(listener_id:int, speaker_id:int):
    result = await db.delete_listener_from_speaker(listener_id, speaker_id)
    result = await db.remove_listener_from_all_lectures(listener_id, speaker_id)

    return {"message": f"Слушатель удален из {result['modified']} лекций"}


@router.post('/save-lecture', status_code=status.HTTP_200_OK)
async def save_lecture_rt(data: LectureRequest):
    return await db.save_lecture(data)


@router.get('/open-lecture', status_code=status.HTTP_200_OK)
async def get_all_lecture_rt(user_id: int):
    return await db.get_all_lectures(user_id)


@router.post('/add-to-speaker', status_code=status.HTTP_200_OK)
async def add_listener_to_speaker_rt(data: SpeakerListener):
    return await db.add_listener_to_speaker(data)


@router.get('/listeners-from-lecture', status_code=status.HTTP_200_OK)
async def get_listener_from_lecture_rt(speaker_id: int, name: str):
    return await db.get_listeners_from_lecture(speaker_id, name)


@router.get('/listeners', status_code=status.HTTP_200_OK)
async def get_listeners_rt(speaker_id: int):
    return await db.get_listeners(speaker_id)


@router.delete('/delete-lecture', status_code=status.HTTP_200_OK)
async def delete_lecture_rt(speaker_id: int, name: str):
    return await db.delete_lecture(speaker_id, name)


@router.post('', status_code=status.HTTP_200_OK)
async def set_user_rt(tg_user: UserCreateUpdate):
    return await db.set_user(tg_user)


@router.put('')
async def update_user():
    pass


@router.delete('')
async def delete_user():
    pass
