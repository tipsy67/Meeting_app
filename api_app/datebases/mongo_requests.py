from datetime import datetime

from bson import Int64, ObjectId
from pymongo import AsyncMongoClient, ReturnDocument

from api_app.schemas import SpeakerListener, SpeakerListenerResponse

# Подключение к MongoDB
client = AsyncMongoClient('mongodb://localhost:27017/')
db = client['meeting_app']
users_collection = db['users']
speaker_listener_collection = db['speaker_listener']
lecture_collection = db['lecture']


async def set_user(user) -> dict:
    """
    находит пользователя по tg_id или создает нового
    """
    now = datetime.now()
    user = await users_collection.find_one_and_update(
        {'_id': user.id},
        {
            '$set': {
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'last_activity': now,
            },
            '$setOnInsert': {'_id': user.id, 'created_at': now, 'is_active': True},
        },
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    return user


async def get_all_speakers():
    pipeline = [
        {'$match': {'is_speaker': True, 'is_active': True}},
        {
            '$project': {
                'username': 1,
                'full_name': {'$concat': ['$first_name', ' ', '$last_name']},
                '_id': 1,
            }
        },
    ]

    speakers_cursor = await users_collection.aggregate(pipeline)
    speakers = await speakers_cursor.to_list(length=None)

    return speakers


async def add_listener_to_speaker(data):
    now = datetime.now()
    link = await speaker_listener_collection.find_one_and_update(
        {'speaker_id': data.speaker_id, 'listener_id': data.listener_id},
        {
            '$setOnInsert': {
                'speaker_id': data.speaker_id,
                'listener_id': data.listener_id,
                'created_at': now,
            }
        },
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )

    return SpeakerListenerResponse(**link)


async def get_listeners(speaker_id: int):

    pipeline = [
        {'$match': {'speaker_id': speaker_id}},
        {
            '$lookup': {
                'from': users_collection.name,
                'localField': 'listener_id',
                'foreignField': '_id',
                'as': 'user_data',
            }
        },
        {'$unwind': '$user_data'},
        {
            '$project': {
                '_id': '$listener_id',
                'username': '$user_data.username',
                'full_name': {
                    '$concat': ['$user_data.first_name', ' ', '$user_data.last_name']
                },
            }
        },
    ]

    listeners_cursor = await speaker_listener_collection.aggregate(pipeline)
    listeners = await listeners_cursor.to_list(length=None)

    return {'listeners': listeners}

async def save_lecture(data):

    name, user_id = data.name.split('_')

    now = datetime.now()
    lecture = await lecture_collection.find_one_and_update(
        {'_id': int(user_id)},
        {
            '$set': {
                'name': name,
                'listeners': data.data,
                'updated_at': now,
            },
        },
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    return lecture


async def get_all_lectures(user_id: int):
    pipeline = [
        {'$match': {'_id': user_id}},
        {
            '$project': {
                'name': 1,
                 'update_at': 1,
            },
        },
        {'$sort': {'update_at': -1}},
    ]
    lectures_cursor = await lecture_collection.aggregate(pipeline)
    lectures = await lectures_cursor.to_list(length=None)

    return {'lectures': lectures}

async def get_listeners_from_lecture(speaker_id: int, name: str):
    pipeline = [
       {'$match': {'_id': Int64(speaker_id), 'name': name}},
       {'$unwind': '$listeners'},
       {
            '$lookup': {
                'from': users_collection.name,
                'localField': 'listeners',
                'foreignField': '_id',
                'as': 'listener_data'
            }
        },
        {'$unwind': '$listener_data'},
        {'$replaceRoot': {'newRoot': '$listener_data'}}
    ]
    
    listeners_cursor = await lecture_collection.aggregate(pipeline)
    listeners = await listeners_cursor.to_list(length=None)

    return {'listeners': listeners}