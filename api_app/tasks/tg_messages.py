import logging

from api_app.core.taskiq_broker import broker
from aiogram import Bot
from api_app.core.config import settings
from api_app.schemas.users import UserResponse
from api_app.datebases.users_requests import get_user

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
async def send_messages_to_users_task(user_ids: list[int], text: str) -> None:
    for user_id in user_ids:
        pass


@broker.task
async def send_messages_about_conference_task(conference_id: int) -> None:
    pass


@broker.task
async def print_task() -> None:
    logger.warning("eeeeee !!!!")
