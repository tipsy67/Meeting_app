"""
Backend for managing conference
with different methods:
Jitsi, Google Meet, Zoom, etc.
"""
from api_app.datebases.conference_requests import get_stream_by_user_id
from api_app.schemas.conferences import ConferenceCreateModel, ConferenceModel, RecordingModel, JitsiRecordingModel
from api_app.schemas.errors import ErrorResponseModel
from api_app.settings import JITSI_BACKEND, GOOGLE_MEET_BACKEND
from google_services.youtube_api_utils import create_broadcast_async


class JitsiConferenceBackend:
    """
    Jitsi Conference Backend.
    This class is used to manage Jitsi conferences.
    """
    def __init__(self, conference: ConferenceCreateModel):
        """
        Initialize the Google Meet conference backend with a conference model.
        """
        self.data = conference
        self.conference_db = ConferenceModel(
            id=self.data.id,
            speaker_id=self.data.speaker_id,
            listeners=self.data.listeners,
            start_datetime=self.data.start_datetime,
            end_datetime=self.data.end_datetime,
            conference_link=self.get_conference_link(),
        )

    def get_conference_link(self) -> str:
        """
        Get the conference link for Google Meet.
        """
        return f"{JITSI_BACKEND['host']}/{self.data.id}"


    @property
    def details(self) -> ConferenceModel:
        """
        Get the details of the Google Meet conference.
        """
        return self.conference_db


    @property
    async def recording_details(self) -> RecordingModel | ErrorResponseModel:
        """
        Check if the conference is being recorded.
        """
        stream = await get_stream_by_user_id(self.data.speaker_id)
        if not stream:
            return ErrorResponseModel(
                detail="Stream not found for the speaker", status_code=404
            )
        broadcast = await create_broadcast_async(
            title=f"broadcast for user#{self.data.speaker_id}",
            start_datetime=self.data.start_datetime,
            end_datetime=self.data.start_datetime,
            stream_id=stream.id,
        )
        if not broadcast:
            return ErrorResponseModel(
                detail="Failed to create broadcast", status_code=500
            )

        recording_object = JitsiRecordingModel(
            conference_id=self.data.id,
            recording_url=f"https://www.youtube.com/live/{broadcast}",
            stream_key=stream.stream_key,
            broadcast_id=broadcast
        )
        return recording_object



class GoogleMeetConferenceBackend:
    """
    Google Meet Conference Backend.
    This class is used to manage Google Meet conferences.
    """
    def __init__(self, conference: ConferenceCreateModel):
        """
        Initialize the Google Meet conference backend with a conference model.
        """
        self.data = conference
        self.conference_db = ConferenceModel(
            id=self.data.id,
            speaker_id=self.data.speaker_id,
            listeners=self.data.listeners,
            start_datetime=self.data.start_datetime,
            end_datetime=self.data.end_datetime,
            conference_link=self.get_conference_link(),
            recording=self.data.recording
        )

    def get_conference_link(self) -> str:
        """
        Get the conference link for Google Meet.
        """
        return f"{GOOGLE_MEET_BACKEND["host"]}/{self.data.id}"

    @property
    def details(self) -> ConferenceModel:
        """
        Get the details of the Google Meet conference.
        """
        return self.conference_db

    @property
    async def recording_details(self) -> RecordingModel | ErrorResponseModel:
        """
        Check if the conference is being recorded.
        """
        return RecordingModel(
            conference_id=self.data.id,
            recording_url=f"https://recordings.google.com/{self.data.id}"
        )


class ConferenceBackend:
    """
    Class for managing different conference backends.
    """
    backend_type: dict = {
        "jitsi": JitsiConferenceBackend,
        "google_meet": GoogleMeetConferenceBackend
    }
    @classmethod
    def init(
            cls,
            backend_name: str,
            conference: ConferenceCreateModel,
    ):
        """
        Get the conference backend by name.

        :param backend_name: The name of the conference backend.
        :param conference: ConferenceCreateModel instance containing conference details.
        :return: ConferenceModel instance for the specified backend.
        """
        backend = cls.backend_type.get(backend_name)
        if not backend:
            raise ValueError(f"Conference backend '{backend_name}' is not supported.")
        conference = backend(conference)
        return conference
