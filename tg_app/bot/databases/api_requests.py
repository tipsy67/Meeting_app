import os

import httpx
from dotenv import load_dotenv

class APIPath:
    BASE_URL = 'http://localhost:8000/users'
    user = f'{BASE_URL}'
    get_speakers = f'{BASE_URL}/speakers'

async def get_speakers():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            APIPath.get_speakers,
        )
    return response.json()

async def set_user(user):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            APIPath.user,
            json={
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name
            }
        )
    if response.status_code != 201:
        return {'status' : f'request error {response.status_code}'}
    return response.json()