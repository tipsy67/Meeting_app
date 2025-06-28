from fastapi import FastAPI

from api_app.routers import users

app = FastAPI()


@app.get('/')
async def root():
    return {'message': 'Hello!'}


app.include_router(users.router)
