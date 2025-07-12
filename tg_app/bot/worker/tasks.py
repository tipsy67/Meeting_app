from tg_app.bot.worker.celery_app import celery


@celery.task
def send_url_to_listeners(url: str, listeners: list[int]):
    pass