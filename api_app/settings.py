"""
Settings for the API application.
"""
import os
from enum import Enum


from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

# Backend for conference management

CONFERENCE_BACKEND = "livekit" # jitsi | google_meet | livekit

JITSI_BACKEND = {
    "host": os.getenv("JITSI_HOST", "https://meet.jit.si"),
}

GOOGLE_MEET_BACKEND = {
    "host": os.getenv("GOOGLE_MEET_HOST", "https://meet.google.com"),
    "credential_dir": os.getenv("GOOGLE_MEET_CREDENTIAL_PATH", "google_meet_credentials.json"),
}

LIVEKIT_BACKEND = {
    "host": os.getenv("JITSI_HOST", "https://localhost:5173"),
}
