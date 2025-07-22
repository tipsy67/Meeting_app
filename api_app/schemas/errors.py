"""
For defining error schemas used in the API.
"""
from pydantic import BaseModel


class ErrorResponseModel(BaseModel):
    """
    Schema for error responses.
    """
    detail: str
    status_code: int = 400
