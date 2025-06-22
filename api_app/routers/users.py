from fastapi import APIRouter
from starlette import status

from api_app.datebases.mongo_requests import set_user, get_speakers
from api_app.schemas import UserCreateUpdate

router = APIRouter(prefix="/users", tags=["users"])

@router.get('/speakers', status_code=status.HTTP_200_OK)
async def get_all_speakers():
    return await get_speakers()


@router.post('', status_code=status.HTTP_201_CREATED)
async def create_user(tg_user: UserCreateUpdate):
    return await set_user(tg_user)


@router.put('/')
async def update_user():
    pass


@router.delete('/')
async def delete_user():
    pass