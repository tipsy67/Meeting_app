from livekit import api
from live_kit_app.config import LIVEKIT_API_KEY, LIVEKIT_API_SECRET


def get_token(user_id: int, name: str, room: str, is_speaker: bool):
    """
    Generate token with grants for conference room
    """
    default_grants = {"room_join": True, "room": room}
    if is_speaker:
        default_grants["room_admin"] = True
    token = (
        api.AccessToken(api_key=LIVEKIT_API_KEY, api_secret=LIVEKIT_API_SECRET)
        .with_identity(str(user_id))
        .with_name(name=name)
        .with_grants(api.VideoGrants(**default_grants))
    )
    return token.to_jwt()
