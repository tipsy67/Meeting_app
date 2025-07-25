import datetime

from api_app.schemas.conferences import ConferenceOutputModel
from api_app.tasks.tg_messages import send_tg_messages_task


async def create_task_for_tg_messages(
    conference: ConferenceOutputModel, time_delta: datetime.timedelta
) -> None:
    # todo: в какой момент формировать текст, чтобы оставить универсальность сообщений
    text = ""
    target_time = conference.start_datetime - time_delta
    if target_time > datetime.datetime.now():
        await send_tg_messages_task.kiq(
            user_ids=conference.user_ids, text=text, eta=target_time
        )


async def send_messages_about_conference(conference: ConferenceOutputModel):
    text = ""
    await create_task_for_tg_messages(conference, datetime.timedelta(days=1))
    await create_task_for_tg_messages(conference, datetime.timedelta(hours=1))
    await create_task_for_tg_messages(conference, datetime.timedelta(minutes=10))


async def send_messages_for_users(user_ids: list[int], text: str) -> None:
    await send_tg_messages_task.kiq(
        user_ids=user_ids,
        text=text,
    )
