from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from api_app.core.config import settings
from api_app.core.taskiq_broker import broker, redis_source
from api_app.routers import conference, lectures, users


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # startup
    if not broker.is_worker_process:
        await broker.startup()
    await redis_source.startup()

    yield
    # shutdown
    if not broker.is_worker_process:
        await broker.shutdown()
    await redis_source.shutdown()


api_main_app = FastAPI(
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)


# Настройка CORS
api_main_app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.api.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)


@api_main_app.get("/")
async def root():
    return {"message": "Hello!"}


api_main_app.include_router(users.router)
api_main_app.include_router(lectures.router)
api_main_app.include_router(conference.router)
