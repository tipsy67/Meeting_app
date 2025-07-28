import logging
import datetime
from typing import Iterable

from api_app.core.taskiq_broker import broker
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


@broker.task
async def send_individual_message_to_users_task(user_id: int, text: str) -> None:
    async with Bot(token=settings.tg.token) as bot:
        message_id=await bot.send_message(user_id, text)


async def create_task_for_tg_messages(
    conference: ConferenceCreateModel,
    time_delta: datetime.timedelta,
    text: str
) -> None:
    recipients_ids = [user["user_id"] for user in conference.listenerers]
    recipients_info = await get_users(recipients_ids)
    recipients_token = {user["user_id"]: user["id"] for user in conference.listeners}
    target_time = conference.start_datetime - time_delta
    if target_time > datetime.datetime.now():
        for recipient in recipients_info:
            full_message = (f"Здравствуйте, {recipient.first_name} {recipient.last_name} ({recipient.username})"
                            f", {text}?token={recipients_token[recipient.id]} ."
                            f" Начало конференции через {str(time_delta)}")
            await send_individual_message_to_users_task.kiq(
                user_id=recipient.id, text=full_message, eta=target_time
            )


@broker.task
async def send_messages_about_conference_task(conference_id: str) -> None:
    conference = await get_conference(conference_id)
    speaker = await get_user(conference.speaker.user_id)
    text = (f"вас приглашают на конференцию, которая состоится {conference.start_datetime.strftime("%d.%m.%Y")}"
            f" в {conference.start_datetime.strftime("%H:%M")}."
            f" Спикер {speaker.first_name} {speaker.last_name} ({speaker.username})."
            f" Ориентировочная длительность {conference.duration} минут."
            f" Ссылка для перехода {conference.conference_link}")
    await create_task_for_tg_messages(conference, datetime.timedelta(minutes=10), text=text)
    await create_task_for_tg_messages(conference, datetime.timedelta(hours=1), text=text)
    await create_task_for_tg_messages(conference, datetime.timedelta(days=1), text=text)


@broker.task
async def print_task() -> None:
    logger.warning("eeeeee !!!!")
