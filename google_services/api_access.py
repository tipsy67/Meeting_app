"""
Module for access token for google services
"""

import os

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow


SCOPES = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/calendar"
    ]

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
CRED_PATH = os.path.join(CURRENT_DIR, "credentials", "credentials.json")

def get_access_token():
    """
    Auth creds staff for working with api
    """
    creds = None
    # The file credentials.json stores the user's access and refresh tokens,
    # and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(CRED_PATH):
        creds = Credentials.from_authorized_user_file(
            CRED_PATH,
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
                    CRED_PATH, SCOPES
                )
                creds = flow.run_local_server(port=0)
            except Exception as e:
                print(f"Error to flow: {e}")
        # Save the credentials for the next run
        with open(CRED_PATH, "w",
                  encoding="utf-8") as token:
            token.write(creds.to_json())
    if creds and isinstance(creds, Credentials):
        access_token = creds.token
        return access_token
    return
