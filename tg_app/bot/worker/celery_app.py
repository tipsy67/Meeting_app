import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()
celery = Celery(__name__)

celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")

if os.environ.get("CELERY_TIMEZONE"):
    celery.conf.timezone = os.environ["CELERY_TIMEZONE"]