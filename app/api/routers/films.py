from fastapi import APIRouter

route = APIRouter(prefix="/films")

@route.get("/")
async def getAllFilms():
    return {
        "content": "lista de Filmes"
    }
