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

class ConferenceBackends(str, Enum):
    LIVEKIT = "livekit"
    JITSI = "jitsi"
    GOOGLE_MEET = "google_meet"

class LiveKitSettings(BaseModel):
    host: str = "https://localhost:5173"

class GoogleMeetSettings(BaseModel):
    host: str = "https://meet.google.com"
    credential_dir: str = "google_meet_credentials.json"

class JitsiSettings(BaseModel):
    host: str = "https://meet.jit.si"


class ConferenceSettings(BaseModel):
    backend_default: ConferenceBackends = ConferenceBackends.LIVEKIT
    livekit: LiveKitSettings = LiveKitSettings()
    google_meet: GoogleMeetSettings = GoogleMeetSettings()
    jitsi: JitsiSettings = JitsiSettings()

    @property
    def backend(self) -> LiveKitSettings|GoogleMeetSettings|JitsiSettings|None:
        if self.backend_default == ConferenceBackends.LIVEKIT:
            return self.livekit
        elif self.backend_default == ConferenceBackends.GOOGLE_MEET:
            return self.google_meet
        elif self.backend_default == ConferenceBackends.JITSI:
            return self.jitsi


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env.dan',
        case_sensitive=False,
        env_nested_delimiter='__',
        extra='allow')
    conference: ConferenceSettings = ConferenceSettings()


settings = Settings()
print(settings.model_dump())
print(settings.conference.backend)