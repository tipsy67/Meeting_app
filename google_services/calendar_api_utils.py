"""
Module for Google Calendar API utilities.
Manage events & meets
"""
import datetime
from google_services.api_access import get_access_token
import httpx


def create_event(
        summary: str,
        start_time: str,
        end_time: str,
        description: str = "",
) -> dict | None:
    """
    Create a calendar event.
    :param summary: Event title.
    :param start_time: Start time in RFC3339 format.
    :param end_time: End time in RFC3339 format.
    :param description: Event description.
    :param location: Event location.
    :return: Event details or None if failed.
    """
    try:
        access_token = get_access_token()
    except Exception as e:
        print(f"Error with access_token at create_event: {e}")
        return None
    
    params = {
        "calendarId": "primary",
        "sendUpdates": "all",
        "conferenceDataVersion": 1,
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    event_data = {
        "summary": summary,
        "start": {"dateTime": start_time, "timeZone": "UTC"},
        "end": {"dateTime": end_time, "timeZone": "UTC"},
        "description": description,
        "conferenceData": {
            "createRequest": {
                "requestId": f"{datetime.datetime.now().isoformat()}",
                "conferenceSolutionKey": {
                    "type": "hangoutsMeet"
                }
            }
        }
    }

    with httpx.Client() as client:
        try:
            response = client.post(
                url="https://www.googleapis.com/calendar/v3/calendars/primary/events",
                params=params,
                json=event_data,
                headers=headers
            )
            response.raise_for_status()
            return response.json()["conferenceData"]["entryPoints"][0]["uri"]
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            print(f"Error creating event: {e}")
    
    return None
