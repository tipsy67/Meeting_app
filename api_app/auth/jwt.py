from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from starlette import status

from api_app.datebases import (
    users_requests as db,
)

from api_app.auth import jwt_utils
from api_app.auth.jwt_utils import TOKEN_TYPE_FIELD, REFRESH_TOKEN_TYPE, ACCESS_TOKEN_TYPE
from api_app.schemas.users import UserResponse

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login/",
)


def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
) -> dict:
    try:
        payload = jwt_utils.decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}",
        )
    return payload


def validate_token_type(
    payload: dict,
    token_type: str,
) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"invalid token type {current_token_type!r} expected {token_type!r}",)


async def get_user_by_token_sub(payload: dict) -> UserResponse:
    try:
        user_id = int(payload.get("sub", ""))
    except (ValueError, TypeError):
        raise HTTPException(status_code=400, detail="Invalid subject in token")

    if user := await db.get_user(user_id):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)",
    )

def get_auth_user_from_token_of_type(token_type: str):
    async def get_auth_user_from_token(
        payload: dict = Depends(get_current_token_payload),
    ) -> UserResponse:
        validate_token_type(payload, token_type)
        return await get_user_by_token_sub(payload)

    return get_auth_user_from_token

get_user_from_refresh_token = get_auth_user_from_token_of_type(REFRESH_TOKEN_TYPE)
get_user_from_access_token = get_auth_user_from_token_of_type(ACCESS_TOKEN_TYPE)

def get_current_active_auth_user(
    user: UserResponse = Depends(get_user_from_access_token),
) -> UserResponse:
    if user.is_active and not user.is_banned:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="inactive or banned user",
    )