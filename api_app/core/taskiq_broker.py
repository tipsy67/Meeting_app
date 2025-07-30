__all__ = ("broker", "redis_source", "scheduler")

import taskiq_fastapi
from taskiq import TaskiqScheduler
from taskiq_redis import (RedisAsyncResultBackend, RedisScheduleSource,
                          RedisStreamBroker)

# broker = AioPikaBroker(url=settings.rabbitmq.url)
#

result_backend = RedisAsyncResultBackend(
    redis_url="redis://localhost:6379",
)

broker = RedisStreamBroker(
    url="redis://localhost:6379",
).with_result_backend(result_backend)

redis_source = RedisScheduleSource("redis://localhost:6379/0")
scheduler = TaskiqScheduler(broker, sources=[redis_source])

taskiq_fastapi.init(broker, "api_app.main:api_main_app")
