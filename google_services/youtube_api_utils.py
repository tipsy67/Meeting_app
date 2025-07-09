"""
Module for working with Youtube API
"""
import datetime
from google_services.api_access import get_access_token
import httpx


async def create_stream_async(
        title: str
) -> dict | None:
    """
    Create stream
    Need response fields:
        - cdn.streamName: for jitsi config (stream key)
        - id: for save at DB with lecture (one lecture - one stream)
    """
    try:
        access_token = get_access_token()
    except Exception as e:
        print(f"Error with access_token at create_stream: {e}")
    params = {
        "part": "id, snippet, cdn, contentDetails, status"
    }
    data = {
        "snippet": {
            "title": title
        },
        "cdn": {
            "frameRate": "30fps",
            "ingestionType": "rtmp",
            "resolution": "720p"
        }
    }

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                url="https://www.googleapis.com/youtube/v3/liveStreams",
                json=data,
                params=params,
                headers=headers,
            )
            data = response.json()
            return {
                "id": data["id"],
                "stream_key": data["cdn"]["ingestionInfo"]["streamName"],
            }
        except Exception as e:
            print(f"Error with response: {e}")


async def create_broadcast_async(
        title: str,
        start_datetime: datetime,
        end_datetime: datetime,
        stream_id: str
) -> str | None:
    """
    Create broadcast
    Need response fields:
        - id: for create link to recording (https://www.youtube.com/live/<id>)
    Return: url for stream
    """
    try:
        access_token = get_access_token()
    except Exception as e:
        print(f"Error with access_token at create_broadcast: {e}")
    params = {
        "part": "snippet, contentDetails, status"
    }
    data = {
        "snippet": {
            "title": title,
            "scheduledStartTime": start_datetime.isoformat(),
            "scheduledEndTime": end_datetime.isoformat(),
        },
        "status": {"privacyStatus": "unlisted"},
        "contentDetails": {"enableAutoStart": True, "enableAutoStop": True},
    }

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    async with httpx.AsyncClient() as client:
        try:
            broadcast_response = await client.post(
                url="https://youtube.googleapis.com/youtube/v3/liveBroadcasts",
                json=data,
                params=params,
                headers=headers,
            )
            broadcast_data = broadcast_response.json()
            if broadcast_response.status_code == 200:
                params = {
                    "part": "id, snippet, status, contentDetails",
                    "id": broadcast_data["id"],
                    "streamId": stream_id
                }
                headers = {"Authorization": f"Bearer {access_token}"}
                response = await client.post(
                    url="https://www.googleapis.com/youtube/v3/liveBroadcasts/bind",
                    params=params,
                    headers=headers,
                )
                data = response.json()
                return data.get("id")

        except Exception as e:
            print(f"Error with response: {e}")
