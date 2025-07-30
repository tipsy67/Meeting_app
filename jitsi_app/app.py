"""
Jitsi App - FastAPI Application
This application with one page with meeting window.
"""

import os

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from api_app.schemas.errors import ErrorResponseModel
from jitsi_app.utils import get_conference_by_id, get_user_by_id

CUR_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()

app.mount(
    "/static", StaticFiles(directory=os.path.join(CUR_DIR, "static")), name="static"
)

templates = Jinja2Templates(directory=os.path.join(CUR_DIR, "templates_test"))


@app.get("/{conference_id}", response_class=HTMLResponse)
async def index(request: Request, conference_id: str, user_id: int):
    """
    Render the Jitsi meeting page for a specific conference.
    Params: user_id or token
    """
    conference = await get_conference_by_id(conference_id)
    if isinstance(conference, ErrorResponseModel):
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={
                "message": conference.detail,
                "status_code": conference.status_code,
            },
            status_code=conference.status_code,
        )
    if conference.is_ended:
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={"message": "This conference has ended.", "status_code": 410},
            status_code=410,
        )
    listeners = conference.users
    if not listeners:
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={
                "message": "No listeners found for this conference.",
                "status_code": 404,
            },
            status_code=404,
        )
    if user_id not in listeners or user_id != conference.speaker_id:
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={
                "message": "You are not a listener of this conference.",
                "status_code": 403,
            },
            status_code=403,
        )
    current_user = await get_user_by_id(user_id)
    if isinstance(current_user, ErrorResponseModel):
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={
                "message": current_user.detail,
                "status_code": current_user.status_code,
            },
            status_code=current_user.status_code,
        )
    full_name = f"{current_user.first_name}{(' ' + current_user.last_name) if current_user.last_name else ''}"
    # get user detail
    context = {
        "display_name": full_name,
        "user_id": current_user.id,
        "stream_key": conference.stream_key,
        "broadcast_id": conference.broadcast_id,
        "is_speaker": current_user.is_speaker
        and current_user.id == conference.speaker_id,
        "title": f"Conference {conference_id}",
    }
    return templates.TemplateResponse(
        request=request, name="index_jaas.html", context=context
    )
