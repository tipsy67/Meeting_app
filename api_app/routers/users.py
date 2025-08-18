from fastapi import APIRouter, Depends
from starlette import status

from api_app.auth.jwt import get_current_active_auth_user
from api_app.datebases import \
    users_requests as db  # напрямую через функции работающие с БД
from api_app.schemas.users import (ListenersListResponse, SpeakerListener,
                                   SpeakerListenerResponse,
                                   SpeakersListResponse, UserCreateUpdate,
                                   UserResponse)
from api_app.services import \
    users as srv  # через сервисную прослойку для создания отложенных задач

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_current_active_auth_user)],
)

router_unsecure = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
    summary="Получить пользователя из базы",
    description="Получает информацию о пользователе",
)
async def get_user_rt(tg_user_id: int) -> UserResponse:
    return await db.get_user(tg_user_id)


@router_unsecure.post(
    "",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
    summary="Добавить пользователя в базу",
    description="Добавляет пользователя в базу, либо обновляет информацию о нем",
)
async def set_user_rt(tg_user: UserCreateUpdate) -> UserResponse:
    return await db.set_user(tg_user)


@router.get(
    "/speakers",
    status_code=status.HTTP_200_OK,
    response_model=SpeakersListResponse,
    summary="Получить список спикеров",
    description="Возвращает активных спикеров с их username и полным именем",
)
async def get_all_speakers_rt():
    return await db.get_all_speakers()


@router.post(
    "/speakers/listeners",
    status_code=status.HTTP_200_OK,
    response_model=SpeakerListenerResponse,
    summary="Добавить пользователя к лектору",
    description="Добавляет пользователя в слушатели(подписчики) к лектору",
)
async def add_listener_to_speaker_rt(data: SpeakerListener):
    return await srv.add_listener_to_speaker(data)


@router.get(
    "/listeners",
    status_code=status.HTTP_200_OK,
    response_model=ListenersListResponse,
    summary="Получает список слушателей(подписчиков)",
    description="Получает список слушателей(подписчиков) по указанному id спикера",
)
async def get_listeners_rt(speaker_id: int):
    return await db.get_listeners(speaker_id)


@router.get(
    "/listeners/speakers",
    status_code=status.HTTP_200_OK,
    response_model=SpeakersListResponse,
    summary="Получает список спикеров",
    description="Получает список спикеров (на которые подписан слушатель) по указанному id слушателя",
)
async def get_speakers_for_listener_rt(listener_id: int):
    return await db.get_speakers(listener_id)


@router.delete(
    "/listeners/speakers",
    status_code=status.HTTP_200_OK,
    summary="Слушатель отписывается от лектора",
    description="Разрывает связь межу лектором и слушателем по указанным id лектора и слушателя",
)
async def remove_from_listeners_rt(listener_id: int, speaker_id: int):
    return await srv.delete_listener_from_speaker(listener_id, speaker_id)
