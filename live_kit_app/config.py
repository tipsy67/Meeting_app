"""
Config Module for LiveKit App
"""
import os
import dotenv

dotenv.load_dotenv()


LIVEKIT_URL = os.getenv("LIVEKIT_URL")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")

ALLOW_ORIGINS = os.getenv("ALLOW_ORIGINS").split(' ')

API_API_URL=os.getenv("API_API_URL")

TG_TOKEN = os.getenv("TG_TOKEN")
