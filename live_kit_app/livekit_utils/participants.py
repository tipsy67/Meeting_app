"""
Module for manage Participants
LiveKit API
"""
from livekit.api import LiveKitAPI, ListParticipantsRequest
from live_kit_app.config import LIVEKIT_API_KEY, LIVEKIT_API_SECRET, LIVEKIT_URL


async def get_participants(room_name: str):
    """
    participants list
    """
    async with LiveKitAPI(
        url=LIVEKIT_URL,
        api_key=LIVEKIT_API_KEY,
        api_secret=LIVEKIT_API_SECRET
    ) as lkapi:
        response = await lkapi.room.list_participants(ListParticipantsRequest(room=room_name))
        return response
