from datetime import datetime

from api_app.core.taskiq_broker import broker

@broker.task
async def create_messages_for_conference(users: list[int]) -> None:
    pass