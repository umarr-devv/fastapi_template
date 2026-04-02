from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated

from api.v1.repository import *

from .session import get_session


async def get_manager(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> RepositoriesManager:
    return RepositoriesManager(session)
