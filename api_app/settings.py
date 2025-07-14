"""
Settings for the API application.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Backend for conference management

CONFERENCE_BACKEND = "jitsi" # jitsi | google_meet

JITSI_BACKEND = {
    "host": os.getenv("JITSI_HOST", "https://meet.jit.si"),
}

GOOGLE_MEET_BACKEND = {
    "host": os.getenv("GOOGLE_MEET_HOST", "https://meet.google.com"),
    "credential_dir": os.getenv("GOOGLE_MEET_CREDENTIAL_PATH", "google_meet_credentials.json"),
}
