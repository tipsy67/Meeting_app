from livekit.api import WebhookReceiver, TokenVerifier
from live_kit_app.config import LIVEKIT_API_KEY, LIVEKIT_API_SECRET

token = TokenVerifier(
    api_key=LIVEKIT_API_KEY,
    api_secret=LIVEKIT_API_SECRET
)

webhook_receiver = WebhookReceiver(
    token_verifier=token
)
