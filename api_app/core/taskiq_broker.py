__all__ = ("broker",)

import taskiq_fastapi
from taskiq_aio_pika import AioPikaBroker

from api_app.core.config import settings

broker = AioPikaBroker(
    url=settings.rabbitmq.url
)

taskiq_fastapi.init(broker, "main:api_main_app")