from livekit import api
from live_kit_app.config import LIVEKIT_API_KEY, LIVEKIT_API_SECRET



def get_token(name: str, room: str, is_speaker: bool):
    """
    Generate token with grants for conference room
    """
    default_grants = {
        "room_join": True,
        "room": room
    }
    if is_speaker:
        default_grants["room_admin"] = True
    token = api.AccessToken(
        api_key=LIVEKIT_API_KEY,
        api_secret=LIVEKIT_API_SECRET
    ).with_identity(
        "identity"
        ).with_name(
        name=name
        ).with_grants(
            api.VideoGrants(
                room_join=True,
                room=room,
            )
        )
    return token.to_jwt()
