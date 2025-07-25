from datetime import datetime

from pymongo import ReturnDocument

from api_app.datebases import config_base as db
from api_app.schemas.users import (
    SpeakerListenerResponse,
)
from api_app.tasks.tg_messages import send_message_to_speaker_task


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
    await send_message_to_speaker_task(
        initiator_id=data.listener_id,
        recipient_id=data.speaker_id,
        text="на вас подписался",
    )
    return SpeakerListenerResponse(**link)


async def delete_listener_from_speaker(listener_id: int, speaker_id: int):
    result = await db.speaker_listener_collection.find_one_and_delete(
        {"speaker_id": speaker_id, "listener_id": listener_id},
        projection={"_id": False},
    )
    await send_message_to_speaker_task(
        initiator_id=listener_id, recipient_id=speaker_id, text="от вас отписался"
    )
    return {"deleted": result}

