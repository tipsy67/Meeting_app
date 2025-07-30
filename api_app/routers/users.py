from fastapi import APIRouter
from starlette import status

from api_app.datebases import (
    users_requests as db,
)  # напрямую через функции работающие с БД
from api_app.services import (
    users as srv,
)  # через сервисную прослойку для создания отложенных задач

from api_app.schemas.users import (
    SpeakerListener,
    UserCreateUpdate,
    LectureRequest,
    UserResponse,
)
from api_app.tasks.tg_messages import print_task

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/test")
async def test():
    await print_task.kiq()
    return {"status": "ok"}


@router.get("", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user_rt(tg_user_id: int) -> UserResponse:
    return await db.get_user(tg_user_id)


@router.post("", status_code=status.HTTP_200_OK)
async def set_user_rt(tg_user: UserCreateUpdate) -> UserResponse:
    return await db.set_user(tg_user)


@router.get("/speakers", status_code=status.HTTP_200_OK)
async def get_all_speakers_rt():
    return await db.get_all_speakers()


@router.post("/speakers/listeners", status_code=status.HTTP_200_OK)
async def add_listener_to_speaker_rt(data: SpeakerListener):
    return await srv.add_listener_to_speaker(data)


@router.get("/listeners", status_code=status.HTTP_200_OK)
async def get_listeners_rt(speaker_id: int):
    return await db.get_listeners(speaker_id)


@router.get("/listeners/speakers", status_code=status.HTTP_200_OK)
async def get_speakers_for_listener_rt(listener_id: int):
    return await db.get_speakers(listener_id)


@router.delete("/listeners/speakers", status_code=status.HTTP_200_OK)
async def remove_from_listeners_rt(listener_id: int, speaker_id: int):
    return await srv.delete_listener_from_speaker(listener_id, speaker_id)
