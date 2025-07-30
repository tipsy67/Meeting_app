from datetime import datetime

from api_app.core.l10n import l10n
from api_app.datebases import users_requests as db
from api_app.datebases.users_requests import (get_listeners_ids_from_lecture,
                                              get_user)
from api_app.schemas.users import SpeakerListenerResponse, UserResponse
from api_app.tasks.tg_messages import (send_message_to_speaker_task,
                                       send_messages_to_users_task)


async def add_listener_to_speaker(data):
    response = await db.add_listener_to_speaker(data)
    await send_message_to_speaker_task.kiq(
        initiator_id=data.listener_id,
        recipient_id=data.speaker_id,
        alias_text="subscribe",
    )
    return response


async def delete_listener_from_speaker(listener_id: int, speaker_id: int):
    response = await db.delete_listener_from_speaker(listener_id, speaker_id)

    await send_message_to_speaker_task.kiq(
        initiator_id=listener_id, recipient_id=speaker_id, alias_text="unsubscribe"
    )
    return response


async def save_lecture(data):
    speaker_id, lecture_name = data.name.split("_")
    speaker_id = int(speaker_id)

    speaker: UserResponse = await get_user(speaker_id)
    old_lecture: dict = await get_listeners_ids_from_lecture(speaker_id, lecture_name)
    added_listeners = set(data.data)
    removed_listeners = set()
    prev_listeners = old_lecture.get("listeners")

    if prev_listeners is not None and len(prev_listeners) > 0:
        added_listeners = added_listeners - set(prev_listeners)
        removed_listeners = set(prev_listeners) - set(data.data)

    response = await db.save_lecture(data)

    if added_listeners:
        await send_messages_to_users_task.kiq(
            recipients_ids=added_listeners,
            text=f"{speaker.first_name} {speaker.last_name} (@{speaker.username})"
            f" add_to_lecture {lecture_name}",
            alias_text="add_to_lecture",
        )
    if removed_listeners:
        await send_messages_to_users_task.kiq(
            recipients_ids=removed_listeners,
            text=f"{speaker.first_name} {speaker.last_name} ({speaker.username})"
            f" remove_from_lecture {lecture_name}",
            alias_text="remove_from_lecture",
        )

    return response


async def delete_lecture(speaker_id: int, lecture_name: str):
    speaker: UserResponse = await get_user(speaker_id)
    old_lecture: dict = await get_listeners_ids_from_lecture(speaker_id, lecture_name)

    removed_listeners = old_lecture.get("listeners")

    response = await db.delete_lecture(speaker_id, lecture_name)

    if removed_listeners:
        await send_messages_to_users_task.kiq(
            recipients_ids=removed_listeners,
            text=f"{speaker.first_name} {speaker.last_name} ({speaker.username})"
            f" удалил лекцию {lecture_name}",
        )

    return response
