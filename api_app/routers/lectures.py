from fastapi import APIRouter, Depends, HTTPException, Query
from starlette import status

from api_app.auth.jwt import get_current_active_auth_user
from api_app.datebases import \
    users_requests as db  # напрямую через функции работающие с БД
from api_app.schemas.users import (DeleteLectureResponse, LectureRequest,
                                   LectureResponse, LecturesListResponse,
                                   ListenersFromLectureResponse)
from api_app.services import \
    users as srv  # через сервисную прослойку для создания отложенных задач

router = APIRouter(
    prefix="/lectures",
    tags=["lectures"],
    dependencies=[Depends(get_current_active_auth_user)],
)


# Все лекции привязаны к одному спикеру, слушатели как список
@router.post(
    "",
    status_code=status.HTTP_200_OK,
    response_model=LectureResponse,
    summary="Сохранить лекцию",
    description="Сохраняет или обновляет информацию о лекции",
)
async def save_lecture_rt(data: LectureRequest):
    return await srv.save_lecture(data)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=LecturesListResponse,
    summary="Получить список лекций",
    description="Получает список лекций по speaker_id ИЛИ listener_id",
)
async def get_lectures(
    speaker_id: int | None = Query(None, description="ID спикера"),
    listener_id: int | None = Query(None, description="ID слушателя"),
):

    if speaker_id is None and listener_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Необходимо указать либо speaker_id, либо listener_id",
        )

    if speaker_id is not None and listener_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Укажите только один параметр - speaker_id ИЛИ listener_id",
        )
    if speaker_id is not None:
        return await db.get_all_lectures(speaker_id)
    elif listener_id is not None:
        return await db.get_all_lectures_by_listener(listener_id)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Проблемы при получении списка лекций",
        )


@router.delete(
    "",
    status_code=status.HTTP_200_OK,
    response_model=DeleteLectureResponse,
    summary="Удаляет лекцию",
    description="Удаляет лекцию",
)
async def delete_lecture_rt(speaker_id: int, name: str):
    return await srv.delete_lecture(speaker_id, name)


@router.get(
    "/listeners",
    status_code=status.HTTP_200_OK,
    response_model=ListenersFromLectureResponse,
    summary="Получить слушателей из лекции",
    description="Получает список слушателей, которые добавлены в лекцию",
)
async def get_listener_from_lecture_rt(speaker_id: int, name: str):
    return await db.get_listeners_from_lecture(speaker_id, name)


@router.delete(
    "/listeners-unsubscribe",
    status_code=status.HTTP_200_OK,
    summary="Отписаться от спикера",
    description="Слушатель отписывается от лектора и удаляется из всех подписок на лекции",
)
async def remove_from_listeners_rt(listener_id: int, speaker_id: int):
    result = await srv.delete_listener_from_speaker(listener_id, speaker_id)
    result = await db.remove_listener_from_all_lectures(listener_id, speaker_id)

    return {"deleted": f"{result['modified']}"}


@router.delete(
    "/listeners-unsubscribe-lecture",
    status_code=status.HTTP_200_OK,
    summary="Отписаться от лекции",
    description="Слушатель отписывается от лекции",
)
async def remove_from_listeners_rt(listener_id: int, lecture: str):

    result = await db.remove_listener_from_lecture(listener_id, lecture)

    return {"deleted": f"{result['modified']}"}
