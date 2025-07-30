from datetime import datetime
from typing import Iterable

from fastapi import HTTPException
from pymongo import ReturnDocument
from starlette import status

from api_app.datebases import config_base as db
from api_app.schemas.users import (
    SpeakerListenerResponse,
    UserCreateUpdate,
    UserResponse,
)


async def get_user(tg_user_id: int) -> UserResponse:
    """
    находит пользователя по tg_id
    """
    if user := await db.users_collection.find_one({"_id": tg_user_id}):
        return UserResponse(**user)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"User {tg_user_id} not found"
    )


async def get_users(recipients_ids: Iterable[int]) -> list[UserResponse]:
    id_list = list(recipients_ids)
    cursor = db.users_collection.find({"_id": {"$in": id_list}})

    return [UserResponse(**user) async for user in cursor]


async def set_user(tg_user: UserCreateUpdate) -> UserResponse:
    """
    находит пользователя по tg_id для изменения данных о нем или создает нового
    """
    now = datetime.now()
    user = await db.users_collection.find_one_and_update(
        {"_id": tg_user.id},
        {
            "$set": {
                "username": tg_user.username,
                "first_name": tg_user.first_name,
                "last_name": tg_user.last_name,
                "last_activity": now,
                "language_code": tg_user.language_code,
            },
            "$setOnInsert": {"_id": tg_user.id, "created_at": now, "is_active": True},
        },
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    return UserResponse(**user)


async def get_all_speakers():
    pipeline = [
        {"$match": {"is_speaker": True, "is_active": True}},
        {
            "$project": {
                "username": 1,
                "full_name": {"$concat": ["$first_name", " ", "$last_name"]},
                "_id": 1,
            }
        },
    ]

    speakers_cursor = await db.users_collection.aggregate(pipeline)
    speakers = await speakers_cursor.to_list(length=None)

    return {"speakers": speakers}


async def get_speakers(listener_id: int):
    pipeline = [
        {"$match": {"listener_id": listener_id}},
        {
            "$lookup": {
                "from": db.users_collection.name,
                "localField": "speaker_id",
                "foreignField": "_id",
                "as": "user_data",
            }
        },
        {"$unwind": "$user_data"},
        {
            "$project": {
                "_id": "$speaker_id",
                "username": "$user_data.username",
                "full_name": {
                    "$concat": ["$user_data.first_name", " ", "$user_data.last_name"]
                },
            }
        },
    ]

    speakers_cursor = await db.speaker_listener_collection.aggregate(pipeline)
    speakers = await speakers_cursor.to_list(length=None)

    return {"speakers": speakers}


async def get_listeners(speaker_id: int):

    pipeline = [
        {"$match": {"speaker_id": speaker_id}},
        {
            "$lookup": {
                "from": db.users_collection.name,
                "localField": "listener_id",
                "foreignField": "_id",
                "as": "user_data",
            }
        },
        {"$unwind": "$user_data"},
        {
            "$project": {
                "_id": "$listener_id",
                "username": "$user_data.username",
                "full_name": {
                    "$concat": ["$user_data.first_name", " ", "$user_data.last_name"]
                },
            }
        },
    ]

    listeners_cursor = await db.speaker_listener_collection.aggregate(pipeline)
    listeners = await listeners_cursor.to_list(length=None)

    return {"listeners": listeners}


async def add_listener_to_speaker(data):
    now = datetime.now()
    link = await db.speaker_listener_collection.find_one_and_update(
        {"speaker_id": data.speaker_id, "listener_id": data.listener_id},
        {
            "$setOnInsert": {
                "speaker_id": data.speaker_id,
                "listener_id": data.listener_id,
                "created_at": now,
            }
        },
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )

    return SpeakerListenerResponse(**link)


async def delete_listener_from_speaker(listener_id: int, speaker_id: int):
    result = await db.speaker_listener_collection.find_one_and_delete(
        {"speaker_id": speaker_id, "listener_id": listener_id},
        projection={"_id": False},
    )

    return {"deleted": result}


async def get_all_lectures(speaker_id: int):
    pipeline = [
        {"$match": {"speaker_id": speaker_id}},
        {
            "$project": {
                "_id": "$speaker_id",
                "name": "$lecture_name",
                "update_at": 1,
            },
        },
        {"$sort": {"update_at": -1}},
    ]
    lectures_cursor = await db.lecture_collection.aggregate(pipeline)
    lectures = await lectures_cursor.to_list(length=None)

    return {"lectures": lectures}


async def get_listeners_ids_from_lecture(speaker_id: int, name: str) -> dict:
    lecture = await db.lecture_collection.find_one(
        {"speaker_id": speaker_id, "lecture_name": name}, {"listeners": 1}
    )
    return {"listeners": lecture.get("listeners", []) if lecture else []}


async def get_listeners_from_lecture(speaker_id: int, name: str) -> dict:
    pipeline = [
        {"$match": {"speaker_id": speaker_id, "lecture_name": name}},
        {"$unwind": "$listeners"},
        {
            "$lookup": {
                "from": db.users_collection.name,
                "localField": "listeners",
                "foreignField": "_id",
                "as": "listener_data",
            }
        },
        {"$unwind": "$listener_data"},
        {"$replaceRoot": {"newRoot": "$listener_data"}},
    ]

    listeners_cursor = await db.lecture_collection.aggregate(pipeline)
    listeners = await listeners_cursor.to_list(length=None)

    return {"listeners": listeners}


async def delete_lecture(speaker_id: int, lecture_name: str):
    result = await db.lecture_collection.find_one_and_delete(
        {"speaker_id": speaker_id, "lecture_name": lecture_name},
        projection={"_id": False},  # это исключение из результата!
    )
    if not result:
        raise HTTPException(status_code=404, detail=f"Lecture {lecture_name} not found")

    return {"deleted": result}


async def remove_listener_from_all_lectures(listener_id: int, speaker_id: int):
    """
    Удаляет слушателя из всех лекций, где он есть в массиве listeners.
    """
    result = await db.lecture_collection.update_many(
        {
            "listeners": listener_id,
            "speaker_id": speaker_id,
        },
        {"$pull": {"listeners": listener_id}},
    )

    return {"matched": result.matched_count, "modified": result.modified_count}


async def save_lecture(data):
    speaker_id, lecture_name = data.name.split("_")
    speaker_id = int(speaker_id)
    now = datetime.now()

    lecture = await db.lecture_collection.find_one_and_update(
        {"speaker_id": speaker_id, "lecture_name": lecture_name},
        {
            "$set": {
                "speaker_id": speaker_id,
                "lecture_name": lecture_name,
                "listeners": data.data,
                "updated_at": now,
            },
        },
        projection={"_id": False},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )

    return lecture
