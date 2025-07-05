"""
Module for working with google API
Youtube & Calendar
"""

import os
import datetime

import httpx

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow


SCOPES = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/calendar"
    ]


def get_access_token():
    """
    Auth creds staff for working with api
    """
    creds = None
    # The file credentials.json stores the user's access and refresh tokens,
    # and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("credentials/credentials.json"):
        creds = Credentials.from_authorized_user_file(
            "credentials/credentials.json",
            SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refresh token: {e}")
        else:
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials/secret_file.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            except Exception as e:
                print(f"Error to flow: {e}")
        # Save the credentials for the next run
        with open("credentials/credentials.json", "w",
                  encoding="utf-8") as token:
            token.write(creds.to_json())
    if creds and isinstance(creds, Credentials):
        access_token = creds.token
        return access_token
    return


async def create_broadcast_async(
        title: str,
        start_time: datetime
):
    """
    Create broadcast
    Need response fields:
        - id: for create link to recording (https://www.youtube.com/live/<id>)
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
            "scheduledStartTime": start_time.isoformat()
        },
        "status": {
            "privacyStatus": "unlisted"
        },
        "contentDetails": {
            "enableAutoStart": True,
            "enableAutoStop": True
        }
    }

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                url="https://youtube.googleapis.com/youtube/v3/liveBroadcasts",
                json=data,
                params=params,
                headers=headers,
            )
            return response.json()
        except Exception as e:
            print(f"Error with response: {e}")


async def create_stream_async(
        title: str
):
    """
    Create stream
    Need response fields:
        - cdn.streamName: for jitsi config (stream key)
        - id: for save at DB with lecture (one lecture - one stream)
    """
    try:
        access_token = get_access_token()
    except Exception as e:
        print(f"Error with access_token at create_broadcast: {e}")
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
            return response.json()
        except Exception as e:
            print(f"Error with response: {e}")


async def bind_broadcast(
        broadcast_id: str,
        stream_id: str
):
    """
    Bind broadcast
    Join broadcast with stream
    """
    try:
        access_token = get_access_token()
    except Exception as e:
        print(f"Error with access_token at create_broadcast: {e}")
    params = {
        "part": "id, snippet, status, contentDetails",
        "id": broadcast_id,
        "streamId": stream_id

    }

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                url=(
                    "https://www.googleapis.com/youtube/v3/"
                    "liveBroadcasts/bind"
                ),
                params=params,
                headers=headers,
            )
            return response.json()
        except Exception as e:
            print(f"Error with response: {e}")

# TODO: create event with meeting at calendar
