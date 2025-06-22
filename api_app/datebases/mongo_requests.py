from pymongo import AsyncMongoClient
from pymongo import ReturnDocument
from datetime import datetime

from api_app.schemas import SpeakerListener, SpeakerListenerResponse

# Подключение к MongoDB
client = AsyncMongoClient("mongodb://localhost:27017/")
db = client["meeting_app"]
users_collection = db["users"]
speaker_listener_collection = db["speaker_listener"]


async def set_user(user) -> dict:
    """
    находит пользователя по tg_id или создает нового
    """
    now = datetime.now()
    user = await users_collection.find_one_and_update(
{'_id': user.id},
        {'$set': {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'last_activity': now,
            },
            '$setOnInsert': {
            '_id': user.id,
            'created_at': now,
            'is_active': True
        }},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )
    return user

async def get_speakers():
    pipeline = [
        {'$match': {'is_speaker': True, 'is_active': True}},

        {'$project': {
            'username': 1,
            'full_name': {
                '$concat': [
                    '$first_name',
                    ' ',
                    '$last_name'
                ]
            },
            '_id': 1
        }}
    ]

    speakers_cursor = await users_collection.aggregate(pipeline)
    speakers = await speakers_cursor.to_list(length=None)

    return speakers

async def add_listener_to_speaker(data):
    now = datetime.now()
    link = await speaker_listener_collection.find_one_and_update(
        {'speaker_id': data.speaker_id, 'listener_id': data.listener_id},
        {'$setOnInsert': {
                'speaker_id': data.speaker_id,
                'listener_id': data.listener_id,
                'created_at': now,
            }},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )

    return SpeakerListenerResponse(**link)