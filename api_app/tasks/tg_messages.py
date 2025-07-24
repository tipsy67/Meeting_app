import logging

from api_app.core.taskiq_broker import broker
from api_app.tasks.utils import bot_send_message

logger = logging.getLogger("taskiq")
logger.setLevel(logging.INFO)
handler = logging.FileHandler('taskiq.log')
logger.addHandler(handler)

@broker.task
async def send_tg_messages_task(user_ids: list[int], text:str) -> None:
    for user_id in user_ids:
        await bot_send_message(user_id, text)

@broker.task
async def print_task() -> None:
    logger.warning("eeeeee !!!!")
