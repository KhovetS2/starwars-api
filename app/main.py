from fastapi import FastAPI
from .api.routers import films

app = FastAPI()

app.include_router(films.route)
