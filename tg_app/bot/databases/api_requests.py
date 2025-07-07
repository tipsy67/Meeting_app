import os
from functools import wraps
from typing import Callable, Optional

import httpx
from aiogram.types import CallbackQuery
from dotenv import load_dotenv


class APIPath:
    BASE_URL = 'http://localhost:8000/users'
    set_user = f'{BASE_URL}'
    get_speakers = f'{BASE_URL}/speakers'
    add_to_speaker = f'{BASE_URL}/add-to-speaker'
    get_listeners = f'{BASE_URL}/listeners'
    save_lecture = f'{BASE_URL}/save-lecture'
    get_lectures = f'{BASE_URL}/open-lecture'
    delete_lectures = f'{BASE_URL}/delete-lecture'
    get_listeners_from_lecture = f'{BASE_URL}/listeners-from-lecture'


def httpx_request(method: str = 'POST', url: str = None, status_code: int = 200):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request_data = await func(*args, **kwargs)

            async with httpx.AsyncClient() as client:
                http_method = getattr(client, method.lower())
                request_args = {
                    'url': url,
                }

                if request_data:
                    for key in ['params', 'headers', 'json', 'data']:
                        if (value := request_data.get(key)) is not None:
                            request_args[key] = value

                response = await http_method(**request_args)

                if response.status_code != status_code:
                    return {
                        'error': f'Request error {response.status_code}',
                        'details': response.text,
                    }

                return response.json()

        return wrapper

    return decorator


@httpx_request(method='GET', url=APIPath.get_speakers)
async def get_speakers():
    return None


@httpx_request(method='POST', url=APIPath.set_user)
async def set_user(user):
    json = {
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }

    return {'json': json}


@httpx_request(method='POST', url=APIPath.add_to_speaker)
async def add_speaker(speaker: int, listener: int):
    json = {
        'speaker_id': speaker,
        'listener_id': listener,
    }

    return {'json': json}


@httpx_request(method='GET', url=APIPath.get_listeners)
async def get_listeners(speaker: int):
    params = {
        'speaker_id': speaker,
    }

    return {'params': params}


@httpx_request(method='POST', url=APIPath.save_lecture)
async def save_lecture(name_lecture: str, set_listeners: set[int]):
    json = {
        'name': name_lecture,
        'data': list(set_listeners),
    }
    print(json)
    return {'json': json}


@httpx_request(method='GET', url=APIPath.get_lectures)
async def get_all_lectures(user_id: int):
    params = {
        'user_id': user_id,
    }

    return {'params': params}


@httpx_request(method='GET', url=APIPath.get_listeners_from_lecture)
async def get_listeners_from_lecture(speaker_id: int, name: str):
    params = {
        'speaker_id': speaker_id,
        'name': name,
    }

    return {'params': params}


@httpx_request(method='DELETE', url=APIPath.delete_lectures, status_code=200)
async def delete_lectures(speaker_id: int, name: str):
    params = {
        'speaker_id': speaker_id,
        'name': name,
    }

    return {'params': params}
