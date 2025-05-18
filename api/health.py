import logging

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy import text
from typing_extensions import Annotated

from deps import get_repositories
from repositories import RepositoryManager
from schemes import HealthScheme

router = APIRouter(prefix='/health', tags=['health'])


@router.get(
    path='/health',
    response_model=HealthScheme
)
async def on_health(
        rep_manager: Annotated[RepositoryManager, Depends(get_repositories)],
):
    try:
        await rep_manager.session.execute(text('SELECT 0'))
    except Exception as exc:
        logging.warning(exc)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="database connection failed"
        )
    return HealthScheme(
        status='Ok'
    )
