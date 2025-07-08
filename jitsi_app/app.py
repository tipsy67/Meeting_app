"""
Jitsi App - FastAPI Application
This application with one page with meeting window.
"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from api_app.schemas.conferences import ConferenceModel
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.post("/conference")
async def create_conference(conference: ConferenceModel):
    """
    Create conference
    """
    pass


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """
    Params: token
    """
    context = {
        "display_name": "context_name",
        "user_id": "123456",
        "stream_key": "test-key"
    }
    return templates.TemplateResponse(
        request=request,
        name="index_jaas copy.html",
        context=context
    )
