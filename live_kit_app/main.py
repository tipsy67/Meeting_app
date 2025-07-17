"""
Main module for LiveKit App
"""
from fastapi import FastAPI
from live_kit_app.livekit_utils.token import get_token
from fastapi.middleware.cors import CORSMiddleware
from live_kit_app.config import ALLOW_ORIGINS

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/get-token")
def get_token_rt(name: str, room: str, is_speaker: bool = False):
    """
    Genereate user`s token for room
    """
    response = get_token(name=name, room=room, is_speaker=is_speaker)
    return {"access_token": response}