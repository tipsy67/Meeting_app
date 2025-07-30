"""
Main module for LiveKit App
"""

from datetime import datetime, timezone

import httpx
from fastapi import (BackgroundTasks, FastAPI, Header, HTTPException, Request,
                     status)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from livekit.api import WebhookEvent
from pydantic import ValidationError

from live_kit_app.config import ALLOW_ORIGINS, API_API_URL
from live_kit_app.livekit_utils.token import get_token
from live_kit_app.livekit_utils.webhooks import webhook_receiver
from live_kit_app.schemas import TelegramMessage
from live_kit_app.telegram_utils import send_message_to_listeners

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/get-token")
def get_token_rt(user_id: int, name: str, room: str, is_speaker: bool = False):
    """
    Genereate user`s token for room
    """
    response = get_token(user_id=user_id, name=name, room=room, is_speaker=is_speaker)
    return {"access_token": response}


@app.get("/check_conference/{conference_id}/{participant_id}")
async def check_conference(conference_id: str, participant_id: str):  # -> Conf | Error
    """
    - Check conference (exist | time | is_ended)
        *Send request to api_app: <api_app_host>/conference/<conference_id>
    - Check user (exist at conference)

    :return:
        - status_code=200:
            {
                status: pending | expired | denied | success
                detail: success: {conference, participant} | pending{datetime} | {string}
            }
        - status_code != 200:
            {
                error: string
            }
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{API_API_URL}/conferences/{conference_id}")
            if response.status_code == 200:
                data = response.json()
                start_datetime = data["start_datetime"]
                # check is_ended
                if data.get("is_ended"):
                    return {"status": "expired", "detail": "Conference is ended"}
                # check user is speaker
                speaker = data.get("speaker")
                if not speaker:
                    JSONResponse(
                        content={"error": "Speaker not found"}, status_code=404
                    )
                if speaker.get("id") == participant_id:
                    speaker_id = speaker.get("user_id")
                    speaker_response = await client.get(
                        f"{API_API_URL}/users?tg_user_id={speaker_id}"
                    )
                    if speaker_response.status_code == 200:
                        return {
                            "status": "success",
                            "detail": {
                                "conference": data,
                                "role": "speaker",
                                "participant": speaker_response.json(),
                            },
                        }
                    return JSONResponse(
                        content={"error": "Error with connecting server"},
                        status_code=400,
                    )
                # check user exist at listeners
                listeners = data.get("listeners")
                if listeners:
                    is_participant_exist = [
                        participant
                        for participant in listeners
                        if participant["id"] == participant_id
                    ]
                    if is_participant_exist:
                        # check start time
                        if start_datetime:
                            if datetime.fromisoformat(start_datetime).replace(
                                tzinfo=timezone.utc
                            ) > datetime.now(timezone.utc):
                                return {
                                    "status": "pending",
                                    "detail": {
                                        "start_datetime": datetime.fromisoformat(
                                            start_datetime
                                        )
                                    },
                                }
                            user_id = is_participant_exist[0]["user_id"]
                            user_response = await client.get(
                                f"{API_API_URL}/users?tg_user_id={user_id}"
                            )
                            if user_response.status_code == 200:
                                return {
                                    "status": "success",
                                    "detail": {
                                        "conference": data,
                                        "role": "listener",
                                        "participant": user_response.json(),
                                    },
                                }

                            return JSONResponse(
                                content={"error": "Error with connecting server"},
                                status_code=400,
                            )
                        else:
                            return JSONResponse(
                                content={"error": "Error with start datetime"},
                                status_code=400,
                            )
                return {
                    "status": "denied",
                    "detail": "You are not member of conference",
                }
            return response.json()
        except Exception as e:
            return JSONResponse(  # поменять на raise
                content={"error": str(e)}, status_code=400
            )


# check is moderator ready
@app.get("/is-moderator-ready/{conference_id}")
async def is_moderator_ready(conference_id: str):
    """
    Check - is moderator ready (speaker at conference room)
    Used LiveKit API
    """
    # get participant list
    # check exist speaker at participant list
    pass


# send chat message to tg
@app.post("/send_message_to_tg")
async def send_message_to_tg(
    message: TelegramMessage, background_task: BackgroundTasks
):
    """
    Send message from LiveKit chat to telegram chat
    """
    try:
        print("Получено:", message)  # Лог для отладки
        background_task.add_task(
            send_message_to_listeners,
            conference_id=message.conference_id,
            message=message.text,
            name=message.name,
        )
        return {"status": "success", "data": message}
    except ValidationError as ve:
        print("Ошибка валидации:", ve)
        raise  # FastAPI сам вернёт 422
    except Exception as e:
        print("Ошибка:", e)
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# TODO: add webhook input with livekit events
@app.post("/livekit_webhooks")
async def livekit_webhooks(
    request: Request, authorization: str = Header(..., alias="Authorization")
):
    """
    Webhook for LiveKit
    """
    raw_body = await request.body()
    # 1. валидация подписи + парсинг
    try:
        event = webhook_receiver.receive(
            body=str(raw_body.decode()),
            auth_token=authorization,
        )
        print(event)
    except Exception as e:
        # подпись неверна или токен неподписан LiveKit‑секретом
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    return {"received": True}
