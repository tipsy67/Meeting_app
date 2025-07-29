import logging
import datetime
from typing import Iterable

from taskiq import ScheduledTask

from api_app.core.taskiq_broker import broker, redis_source
from aiogram import Bot
from api_app.core.config import settings
from api_app.datebases.conference_requests import get_conference
from api_app.schemas.conferences import ConferenceOutputModel, ConferenceCreateModel
from api_app.schemas.users import UserResponse
from api_app.datebases.users_requests import get_user, get_users

logger = logging.getLogger("taskiq")
logger.setLevel(logging.INFO)
handler = logging.FileHandler("taskiq.log")
logger.addHandler(handler)


@broker.task
async def send_message_to_speaker_task(
    initiator_id: int, recipient_id: int, text: str
) -> None:

    initiator: UserResponse = await get_user(initiator_id)
    recipient: UserResponse = await get_user(recipient_id)
    full_message = (
        f"Внимание, {recipient.first_name}! "
        f"{text.capitalize()} {initiator.first_name} {initiator.last_name} ({initiator.username})"
    )
    async with Bot(token=settings.tg.token) as bot:
        await bot.send_message(recipient_id, full_message)


@broker.task
async def send_messages_to_users_task(recipients_ids: Iterable[int], text: str) -> None:
    async with Bot(token=settings.tg.token) as bot:
        recipients=await get_users(recipients_ids)
        for recipient in recipients:
            full_message = f"Внимание, {recipient.first_name}! {text.capitalize()}"
            await bot.send_message(recipient.id, full_message)


@broker.task()
async def send_individual_message_to_users_task(user_id: int, text: str) -> None:
    async with Bot(token=settings.tg.token) as bot:
        message_id=await bot.send_message(user_id, text, parse_mode="HTML")



async def create_task_for_tg_messages(
    conference: ConferenceOutputModel,
    time_delta: datetime.timedelta,
    text: str
) -> None:
    recipients_ids = [user.user_id for user in conference.listeners]
    recipients_info = await get_users(recipients_ids)
    recipients_token = {user.user_id: user.id for user in conference.listeners}
    target_time = (conference.start_datetime - time_delta).replace(tzinfo=datetime.timezone.utc)
    current_time = datetime.datetime.now(datetime.timezone.utc)
    if target_time > current_time:
        for recipient in recipients_info:
            full_message = (f"Здравствуйте, {recipient.first_name} {recipient.last_name} ({recipient.username}).\n"
                            f"{text}?token={recipients_token[recipient.id]}'>Ссылка для перехода</a>.\n"
                            f"Название лекции <b>{conference.lecture_name}</b>.\n"
                            f"Начало конференции через {str(time_delta)}")
            await send_individual_message_to_users_task.schedule_by_time(
                redis_source,
                target_time,
                user_id=recipient.id,
                text=full_message
            )
            logger.warning(f"target_time {target_time} in {recipient.id} {type(recipient.id)}")



@broker.task
async def send_messages_about_conference_task(conference_id: str) -> None:
    conference = await get_conference(conference_id)
    speaker = await get_user(conference.speaker.user_id)
    text = (f"Вас приглашают на конференцию, которая состоится <b>{conference.start_datetime.strftime("%d.%m.%Y")}"
            f" в {conference.start_datetime.strftime("%H:%M")}</b>.\n"
            f"Спикер {speaker.first_name} {speaker.last_name} ({speaker.username}).\n"
            f"Ориентировочная длительность <b>{conference.duration}</b> минут.\n"
            f"<a href='{conference.conference_link}")
    await create_task_for_tg_messages(conference, datetime.timedelta(minutes=10), text=text)
    await create_task_for_tg_messages(conference, datetime.timedelta(hours=1), text=text)
    await create_task_for_tg_messages(conference, datetime.timedelta(days=1), text=text)


@broker.task
async def print_task() -> None:
    logger.warning("eeeeee !!!!")
