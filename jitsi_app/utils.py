"""
Utils for the Jitsi app.
This module contains utility functions and constants used in the Jitsi app.
"""

from api_app.datebases.conference_requests import get_conference
from api_app.datebases.config_base import users_collection
from api_app.schemas.conferences import ConferenceModel
from api_app.schemas.errors import ErrorResponseModel
from api_app.schemas.users import UserResponse


async def get_conference_by_id(
    conference_id: str,
) -> ConferenceModel | ErrorResponseModel:
    """
    Get conference by ID.

    :param conference_id: The ID of the conference to retrieve.
    :return: ConferenceModel if found, None otherwise.
    """
    # TODO: change to api request
    request = await get_conference(conference_id)
    return request


async def get_user_by_id(user_id: int) -> UserResponse | ErrorResponseModel:
    """
    Get user by ID.

    :param user_id: The ID of the user to retrieve.
    :return: UserResponse if found, ErrorResponseModel if not found.
    """
    # TODO: change to api request
    user = await users_collection.find_one({"_id": user_id})
    if not user:
        return ErrorResponseModel(detail="User not found", status_code=404)
    user["id"] = user.pop(
        "_id", None
    )  # TODO: сказать Дэну что лучше использовать pydantic model для mongo с alias
    return UserResponse.model_validate(user, by_alias=True)
