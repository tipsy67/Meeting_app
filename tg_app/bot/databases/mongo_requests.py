from pymongo import AsyncMongoClient
from pymongo import ReturnDocument
from datetime import datetime

# Подключение к MongoDB
client = AsyncMongoClient("mongodb://localhost:27017/")
db = client["meeting_app"]
users_collection = db["users"]


async def set_user(user) -> dict:
    """
    находит пользователя по tg_id или создает нового
    """
    now = datetime.now()
    user = await users_collection.find_one_and_update(
{"_id": user.id},
        {"$set": {
            "username": user.username,
            "last_activity": now,
            },
            "$setOnInsert": {
            "_id": user.id,
            "created_at": now,
            "status": "active"
        }},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )
    return user
