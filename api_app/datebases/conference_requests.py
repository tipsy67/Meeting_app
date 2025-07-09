"""
Module for requesting to MongoDB for conference data
"""
from datetime import datetime
from api_app.schemas.conferences import ConferenceModel, StreamModel
from api_app.schemas.errors import ErrorResponseModel
from api_app.datebases import config_base as db

from google_services.youtube_api_utils import create_stream_async, create_broadcast_async

# Colletctions
stream_collection = db.stream_collection
conference_collection = db.conference_collection

# Requests
async def get_stream_by_user_id(user_id: int) -> StreamModel:
    """
    Get stream object by user id
    """
    stream = await stream_collection.find_one({"user_id": user_id})
    if not stream:
        stream_data = await create_stream_async(title=f"stream_for#{user_id}")
        if stream_data:
            new_stream = StreamModel(
                id=stream_data["id"],
                user_id=user_id,
                stream_key=stream_data["stream_key"]
            )
            await stream_collection.insert_one(StreamModel.model_dump(new_stream, by_alias=True))
            return new_stream
    return StreamModel.model_validate(stream, by_alias=True)


async def insert_conference(
        speaker_id: int, 
        listeners: list,
        start_datetime: datetime,
        end_datetime: datetime
        ) -> ConferenceModel | ErrorResponseModel:
    """
    Insert conference object
    :param speaker_id:
    :param listeners
    :return:

    * datetime.now(tz=timezone(timedelta(hours=2)))
    """
    try:
        stream = await get_stream_by_user_id(speaker_id)
        if not stream:
            return ErrorResponseModel(
                detail="Stream not found for the speaker",
                status_code=404
            )
        broadcast = await create_broadcast_async(
            title=f"broadcast for user#{speaker_id}",
            start_datetime=start_datetime,
            end_datetime=start_datetime,
            stream_id=stream.id
        )
        if not broadcast:
            return ErrorResponseModel(
                detail="Failed to create broadcast",
                status_code=500
            )
        conference = ConferenceModel(
            speaker_id=speaker_id,
            users=listeners[:],
            broadcast_id=broadcast,
            stream_key=stream.stream_key,
            recording_url=f"https://youtube.com/live/{broadcast}",
            start_datetime=start_datetime,
            end_datetime=end_datetime
        )
    except Exception as e:
        print(f"Error: {e}")
        return ErrorResponseModel(
            detail=f"Error creating conference: {e}",
            status_code=500
        )

    try:
        await conference_collection.insert_one(ConferenceModel.model_dump(conference, by_alias=True))
        return conference
    except Exception as e:
        if "E11000 duplicate key error" in str(e):
            print("🔁 Duplicate detected")
            return ErrorResponseModel(
                detail="Conference already exists",
                status_code=400
            )
        print("❌ Unexpected DB error:", type(e), e)
        return ErrorResponseModel(
            detail=f"Unexpected error occurred{e}",
            status_code=500
        )
