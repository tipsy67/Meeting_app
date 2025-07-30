import datetime
import logging
from typing import Iterable

from aiogram import Bot

from api_app.core.config import settings
from api_app.core.l10n import l10n
from api_app.core.taskiq_broker import broker, redis_source
from api_app.datebases.conference_requests import get_conference
from api_app.datebases.users_requests import get_user, get_users
from api_app.schemas.conferences import ConferenceOutputModel
from api_app.schemas.users import UserResponse
from api_app.tasks.tg_messages_utils import reference_points

logger = logging.getLogger("taskiq")
logger.setLevel(logging.INFO)
handler = logging.FileHandler("taskiq.log")
logger.addHandler(handler)


@broker.task
async def send_message_to_speaker_task(
    initiator_id: int, recipient_id: int, text: str = None, alias_text: str = None
) -> None:
    initiator: UserResponse = await get_user(initiator_id)
    recipient: UserResponse = await get_user(recipient_id)
    if alias_text:
        text = await l10n.translate(recipient, alias_text)
    full_message = await l10n.translate(
        recipient,
        "attention-message",
        recipient_name=recipient.first_name,
        text=text.capitalize(),
        initiator_name=f"{initiator.first_name} {initiator.last_name}",
        initiator_username=initiator.username,
    )

    async with Bot(token=settings.tg.token) as bot:
        await bot.send_message(recipient_id, full_message)


@broker.task
async def send_messages_to_users_task(
    recipients_ids: Iterable[int], text: str, alias_text: str = None
) -> None:
    async with Bot(token=settings.tg.token) as bot:
        recipients = await get_users(recipients_ids)
        for recipient in recipients:
            if alias_text:
                replace_text = await l10n.translate(recipient, alias_text)
                text = text.replace(alias_text, replace_text)
            full_message = await l10n.translate(
                recipient,
                "attention-message",
                recipient_name=recipient.first_name,
                text=text,
                initiator_name="null",
                initiator_username="null",
            )
            await bot.send_message(recipient.id, full_message)


@broker.task()
async def send_individual_message_to_users_task(user_id: int, text: str) -> None:
    async with Bot(token=settings.tg.token) as bot:
        message_id = await bot.send_message(user_id, text, parse_mode="HTML")


async def create_task_for_listeners(
    conference: ConferenceOutputModel, speaker: UserResponse
) -> None:
    recipients_ids = [user.user_id for user in conference.listeners]
    recipients_info = await get_users(recipients_ids)
    recipients_token = {user.user_id: user.id for user in conference.listeners}
    for timedelta in reference_points.reference_points:
        target_time = await reference_points.check_target_time(
            conference.start_datetime, timedelta)
        if target_time is not None:
            for recipient in recipients_info:
                full_message = await l10n.translate(
                    recipient,
                    "conference-invitation",
                    date=conference.start_datetime.strftime("%d.%m.%Y"),
                    time=conference.start_datetime.strftime("%H:%M"),
                    speaker_name=f"{speaker.first_name} {speaker.last_name}",
                    speaker_username=speaker.username,
                    lecture_name=conference.lecture_name,
                    time_to_start=await l10n.format_time(speaker, timedelta),
                    duration=conference.duration,
                    link=conference.conference_link,
                    token=recipients_token[recipient.id],
                )
                await send_individual_message_to_users_task.schedule_by_time(
                    redis_source, target_time, user_id=recipient.id, text=full_message
                )


async def create_task_for_speaker(
    conference: ConferenceOutputModel, speaker: UserResponse
) -> None:
    for timedelta in reference_points.reference_points:
        target_time = await reference_points.check_target_time(
            conference.start_datetime, timedelta)
        if target_time is not None:
            full_message = await l10n.translate(
                speaker,
                "conference-speaker",
                date=conference.start_datetime.strftime("%d.%m.%Y"),
                time=conference.start_datetime.strftime("%H:%M"),
                lecture_name=conference.lecture_name,
                time_to_start=await l10n.format_time(speaker, timedelta),
                duration=conference.duration,
                link=conference.conference_link,
            )
            await send_individual_message_to_users_task.schedule_by_time(
                redis_source, target_time, user_id=speaker.id, text=full_message
            )


@broker.task
async def send_messages_about_conference_task(conference_id: str) -> None:
    conference = await get_conference(conference_id)
    speaker = await get_user(conference.speaker.user_id)

    await create_task_for_listeners(conference, speaker)
    await create_task_for_speaker(conference, speaker)


@broker.task
async def print_task() -> None:
    logger.warning("eeeeee !!!!")
