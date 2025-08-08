from fastapi import APIRouter
from fastapi.params import Depends

from api_app.auth.jwt_utils import create_access_token, create_refresh_token
from api_app.auth.telegram import TelegramAuth
from api_app.schemas.auth import TokenInfo
from api_app.schemas.users import UserCreateUpdate
from api_app.datebases import users_requests as db
router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenInfo)
async def login(tg_user: UserCreateUpdate = Depends(TelegramAuth())):
    user_data = await db.set_user(tg_user)
    access_token = create_access_token(user_data)
    refresh_token = create_refresh_token(user_data)
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )

@router.post("/refresh", response_model=TokenInfo, response_model_exclude_none=True)
async def refresh(tg_user: UserCreateUpdate = Depends(get_user_from_refresh)):
    access_token = create_access_token(tg_user)
    return TokenInfo(
        access_token=access_token,
    )