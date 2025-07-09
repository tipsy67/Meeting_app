from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api_app.routers import users, conference

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",  
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
    "https://algaq9-37-44-40-134.ru.tuna.am"
]

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"]
)


@app.get('/')
async def root():
    return {'message': 'Hello!'}


app.include_router(users.router)
app.include_router(conference.router)
