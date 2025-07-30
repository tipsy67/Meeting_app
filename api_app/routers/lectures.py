from fastapi import APIRouter
from starlette import status

from api_app.datebases import \
    users_requests as db  # напрямую через функции работающие с БД
from api_app.schemas.users import LectureRequest
from api_app.services import \
    users as srv  # через сервисную прослойку для создания отложенных задач

router = APIRouter(prefix="/lectures", tags=["lectures"])


# Все лекции привязаны к одному спикеру, слушатели как список
@router.post("", status_code=status.HTTP_200_OK)
async def save_lecture_rt(data: LectureRequest):
    return await srv.save_lecture(data)


@router.get("", status_code=status.HTTP_200_OK)
async def get_all_lecture_rt(speaker_id: int):
    return await db.get_all_lectures(speaker_id)


@router.delete("", status_code=status.HTTP_200_OK)
async def delete_lecture_rt(speaker_id: int, name: str):
    return await srv.delete_lecture(speaker_id, name)


@router.get("/listeners", status_code=status.HTTP_200_OK)
async def get_listener_from_lecture_rt(speaker_id: int, name: str):
    return await db.get_listeners_from_lecture(speaker_id, name)


@router.delete("/listeners-unsubscribe", status_code=status.HTTP_200_OK)
async def remove_from_listeners_rt(listener_id: int, speaker_id: int):
    result = await srv.delete_listener_from_speaker(listener_id, speaker_id)
    result = await db.remove_listener_from_all_lectures(listener_id, speaker_id)

    return {"deleted": f"{result['modified']}"}
