"""Star Wars API Main Application."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import get_settings
from app.infrastructure.db.database import Database
from app.api.routers import (
    films_router,
    people_router,
    planets_router,
    species_router,
    starships_router,
    vehicles_router,
    auth_router,
    users_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    await Database.connect()
    yield
    # Shutdown
    await Database.disconnect()


settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API RESTful que consome dados da SWAPI e expõe endpoints filtráveis para Star Wars.",
    lifespan=lifespan,
)

# Include routers with /api/v1 prefix
app.include_router(films_router, prefix="/api/v1")
app.include_router(people_router, prefix="/api/v1")
app.include_router(planets_router, prefix="/api/v1")
app.include_router(species_router, prefix="/api/v1")
app.include_router(starships_router, prefix="/api/v1")
app.include_router(vehicles_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")


@app.get("/", tags=["Health"])
async def root():
    """Root endpoint for health check."""
    return {
        "message": "Welcome to Star Wars API",
        "docs": "/docs",
        "version": settings.APP_VERSION,
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
