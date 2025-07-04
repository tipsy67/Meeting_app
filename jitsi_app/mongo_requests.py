"""
Module for requesting to MongoDB
"""
from pymongo import AsyncMongoClient
from schemas import User, Speaker, SpeakerInDB, SpeakerOut, Lecture, Conference

from pymongo.errors import DuplicateKeyError


# Connect to DB
client = AsyncMongoClient('mongodb://localhost:27017/')
db = client['meeting_app']

# Collections
user_collection = db["users"]
speakers_collection = db["speakers"]
lecture_collection = db["lectures"]
conference_collection = db["conference"]


async def insert_user(user: User):
    """
    Create user
    """
    try:
        await user_collection.insert_one(user.model_dump(by_alias=True))
        return user
    except DuplicateKeyError:
        return {"error": "Dublikate key!"}


async def get_user(user_id: int):
    """
    Get user by id
    """
    user = await user_collection.find_one({"_id": user_id})
    if user:
        return User.model_validate(user)
    

async def get_users():
    """
    Get list users
    """
    users = user_collection.find()
    return [User.model_validate(user) async for user in users]


async def get_speaker_by_user_id(user_id: str):
    """
    Get speaker by user_id (telegram id)
    """
    speaker = await speakers_collection.find_one({"user_id": user_id})
    return Speaker.model_validate(speaker) if speaker else None



async def insert_speaker(speaker: SpeakerInDB):
    """
    Create speaker from User
    """
    try:
        user_id = speaker.user_id
        is_excist = await get_speaker_by_user_id(user_id)
        # checking if speaker with this user_id
        if is_excist:
            return {"error": "Speaker with user_id may be only one!"}
        await speakers_collection.insert_one(speaker.model_dump(by_alias=True))
        user = await get_user(user_id)
        speaker_out = SpeakerOut(
            id=speaker.id,
            user=user
        )
        return speaker_out
    except DuplicateKeyError:
        return {"error": "Dublikate key!"}
    

async def insert_lecture(lecture: Lecture):
    """
    Create lecture
    """
    await lecture_collection.insert_one(lecture.model_dump(by_alias=True))


async def get_lecture(lecture_id: str):
    """
    Get lecture by id
    """
    lecture = await lecture_collection.find_one({"_id": lecture_id})
    return Lecture.model_validate(lecture) if lecture else None


async def get_lectures(filter: dict = None):
    """
    Get list of lectures
    """
    lectures = lecture_collection.find(filter)
    return [Lecture.model_validate(lecture) async for lecture in lectures]



async def insert_conference(conference: Conference):
    """
    Create conference
    """
    await conference_collection.insert_one(conference.model_dump(by_alias=True))


async def get_conference_by_id(conference_id: str):
    """
    Get conference by id
    """
    conference = await conference_collection.find_one({"_id": conference_id})
    return Conference.model_validate(conference) if conference else None


if __name__ == "__main__":
    user = User(
        _id="12345",
        first_name="test12345"
    )
    async def main():
        await insert_user(
            user=user
        )
    import asyncio

    asyncio.run(main())
