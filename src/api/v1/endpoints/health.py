from datetime import datetime
from typing import Annotated

from aiocache import cached
from fastapi import APIRouter, Depends
from fastapi import File as FastAPIFile
from fastapi import HTTPException, Path, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy import text

from api.v1.dependencies import *
from api.v1.repository import *
from api.v1.schemas import *
from core.logger import logging
from services import *

router = APIRouter(prefix="/health", tags=["health"])


@router.get(path="/db", response_model=DBHealthSchema, operation_id="db_health")
async def on_db_health(
    manager: Annotated[RepositoriesManager, Depends(get_manager)],
):
    try:
        await manager.session.execute(text("SELECT 0"))
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="database connection failed",
        )
    return DBHealthSchema(status="Ok")


@router.get(
    path="/cache", response_model=CacheHealthSchema, operation_id="cache_health"
)
@cached(ttl=60)
async def on_cache_health():
    return CacheHealthSchema(date=datetime.now())
