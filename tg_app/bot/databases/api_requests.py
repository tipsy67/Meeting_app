import os
from functools import wraps
from typing import Callable, Optional

import httpx
from dotenv import load_dotenv

class APIPath:
    BASE_URL = 'http://localhost:8000/users'
    set_user = f'{BASE_URL}'
    get_speakers = f'{BASE_URL}/speakers'
    add_to_speaker = f'{BASE_URL}/add-to-speaker'


def httpx_request(
        method: str = 'POST',
        url: str = None,
        status_code: int = 200
):
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
                    # request_args['params'] = request_data.get('params'),
                    # request_args['headers'] = request_data.get('headers')
                    request_args['json'] = request_data.get('json')

                print(request_args)

                response = await http_method(**request_args)

                if response.status_code != status_code:
                    return {
                        'error': f'Request error {response.status_code}',
                        'details': response.text
                    }

                return response.json()
        return wrapper
    return decorator

@httpx_request(method='GET', url=APIPath.get_speakers)
async def get_speakers():
    return None


@httpx_request(method='POST', url=APIPath.set_user)
async def set_user(user):
    json={
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name
    }

    return {'json': json}

@httpx_request(method='POST', url=APIPath.add_to_speaker)
async def add_speaker(speaker: int, listener: int):
    json={
        'speaker_id': speaker,
        'listener_id': listener,
    }

    return {'json': json}
