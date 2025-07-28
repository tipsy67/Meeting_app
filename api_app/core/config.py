"""
Settings for the API application.
"""

from enum import Enum

from pydantic import BaseModel, AmqpDsn, Field, Extra
from pydantic_settings import BaseSettings, SettingsConfigDict


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
    def backend(self) -> LiveKitSettings | GoogleMeetSettings | JitsiSettings:
        if self.backend_default == ConferenceBackends.LIVEKIT:
            return self.livekit
        elif self.backend_default == ConferenceBackends.GOOGLE_MEET:
            return self.google_meet
        elif self.backend_default == ConferenceBackends.JITSI:
            return self.jitsi


class RabbitMQSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env",),
        case_sensitive=False,
        env_nested_delimiter="__",
        extra="ignore",
    )
    user: str = Field("guest", alias="RABBITMQ_USER")
    password: str = Field("guest", alias="RABBITMQ_PASSWORD")
    host: str = Field("localhost", alias="RABBITMQ_HOST")


    @property
    def url(self):
        return f"amqp://{self.user}:{self.password}@{self.host}:5672"


class TGSettings(BaseModel):
    token: str = ""


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(
            "api_app/.env",
            "api_app/.env.dan",
            # "api_app/.env.production",
        ),  # todo: убрать прямой путь и сделать относительный путь
        case_sensitive=False,
        env_nested_delimiter="__",
        extra="ignore",
    )
    conference: ConferenceSettings = ConferenceSettings()
    rabbitmq: RabbitMQSettings = RabbitMQSettings()
    tg: TGSettings = TGSettings()


settings = Settings()
# print(settings.model_dump())
# print(settings.rabbitmq.url)
