from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

router = APIRouter()


@router.get("/db-health")
async def db_health(
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        text("SELECT 1")
    )

    return {
        "status": "healthy",
        "result": result.scalar()
    }