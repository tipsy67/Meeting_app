"""
Jitsi App - FastAPI Application
This application with one page with meeting window.
"""
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from jitsi_app.mongo_requests import insert_user, get_user, insert_speaker
from jitsi_app.schemas import User, Speaker, SpeakerInDB, SpeakerOut, \
     Conference

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.post("/users")
async def create_user(user: User):
    """
    Create user
    """
    try:
        response = await insert_user(user)
        if response:
            return JSONResponse(
                status_code=400,
                content=response
            )
        return user
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"error": e}
        )


@app.post("/speakers")
async def create_speaker(speaker: Speaker):
    """
    Create speaker
    """
    try:
        user = await get_user(speaker.user_id)
        if user:
            speaker_to_db = SpeakerInDB(
                user_id=user.id
            )
            response = await insert_speaker(speaker_to_db)
            if isinstance(response, SpeakerOut):
                return response
            return JSONResponse(
                status_code=400,
                content=response
            )
        return JSONResponse(
            status_code=400,
            content={"error": "User not found"},
        )
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=400
        )


@app.post("/conference")
async def create_conference(conference: Conference):
    """
    Create conference
    """
    # broadcast
    # get stream_key
    # bind brodcast
    pass
