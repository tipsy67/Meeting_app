"""
Module for manage Rooms
LiveKit API
"""

from livekit.api import (CreateRoomRequest, DeleteRoomRequest,
                         ListRoomsRequest, LiveKitAPI)

from live_kit_app.config import (LIVEKIT_API_KEY, LIVEKIT_API_SECRET,
                                 LIVEKIT_URL)


async def create_room(name: str, max_participants: int):
    """
    Create room
    """
    async with LiveKitAPI(
        url=LIVEKIT_URL, api_key=LIVEKIT_API_KEY, api_secret=LIVEKIT_API_SECRET
    ) as lkapi:
        room = await lkapi.room.create_room(
            CreateRoomRequest(
                name=name, max_participants=max_participants, empty_timeout=10 * 60
            )
        )
        return room


async def get_rooms():
    """
    Room list
    """
    async with LiveKitAPI(
        url=LIVEKIT_URL, api_key=LIVEKIT_API_KEY, api_secret=LIVEKIT_API_SECRET
    ) as lkapi:
        rooms = await lkapi.room.list_rooms(ListRoomsRequest())
        return rooms


async def delete_room(name: str):
    """
    Delete Room
    """
    async with LiveKitAPI(
        url=LIVEKIT_URL, api_key=LIVEKIT_API_KEY, api_secret=LIVEKIT_API_SECRET
    ) as lkapi:
        response = await lkapi.room.delete_room(
            DeleteRoomRequest(
                room=name,
            )
        )
        return response
