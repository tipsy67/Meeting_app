"""
Module for requesting to MongoDB for conference data
"""
from api_app.schemas.conferences import ConferenceModel, YoutubeStreamModel, RecordingModel
from api_app.schemas.errors import ErrorResponseModel
from api_app.datebases import config_base as db

from google_services.youtube_api_utils import create_stream_async

# Collections
stream_collection = db.stream_collection
conference_collection = db.conference_collection
recording_collection = db.recording_collection

# Requests
async def get_stream_by_user_id(user_id: int) -> YoutubeStreamModel:
    """
    Get stream object by user id
    """
    stream = await stream_collection.find_one({"user_id": user_id})
    print(stream)
    if stream is None:
        print("not stream found, creating new one")
        stream_data = await create_stream_async(title=f"stream_for#{user_id}")
        print(stream_data)
        if stream_data:
            new_stream = YoutubeStreamModel(
                id=stream_data["id"],
                user_id=user_id,
                stream_key=stream_data["stream_key"]
            )
            await stream_collection.insert_one(YoutubeStreamModel.model_dump(new_stream, by_alias=True))
            return new_stream
    return YoutubeStreamModel.model_validate(stream, by_alias=True)


async def insert_recording(recording: RecordingModel) -> RecordingModel | ErrorResponseModel:
    """
    Insert recording object into MongoDB.
    """
    try:
        await stream_collection.insert_one(RecordingModel.model_dump(recording))
        return recording
    except Exception as e:
        if "E11000 duplicate key error" in str(e):
            print("🔁 Duplicate detected")
            return ErrorResponseModel(
                detail="Recording already exists",
                status_code=400
            )
        print("❌ Unexpected DB error:", type(e), e)
        return ErrorResponseModel(
            detail=f"Unexpected error occurred{e}",
            status_code=500
        )


async def insert_conference(conference: ConferenceModel) -> ConferenceModel  | ErrorResponseModel:
    """
    Insert conference object into MongoDB.

    * datetime.now(tz=timezone(timedelta(hours=2)))
    """
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

async def get_conference(conference_id: str) -> ConferenceModel | ErrorResponseModel:
    """
    Get conference by id
    :param conference_id:
    :return:
    """
    try:
        conference = await conference_collection.find_one({"_id": conference_id})
        print(conference)
        if not conference:
            return ErrorResponseModel(
                detail="Conference not found",
                status_code=404
            )
        return ConferenceModel.model_validate(conference, by_alias=True)
    except Exception as e:
        print(f"Error: {e}")
        return ErrorResponseModel(
            detail=f"Error retrieving conference: {e}",
            status_code=500
        )
