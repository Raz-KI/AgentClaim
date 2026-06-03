"""API router — aggregates route modules."""
from fastapi import APIRouter
from app.api.routes.health import router as health_router
from app.api.routes.db_health import (
    router as db_health_router
)
api_router = APIRouter()

api_router.include_router(
    health_router,
    tags = ["Health"]
)


api_router.include_router(
    db_health_router,
    tags=["Database"]
)