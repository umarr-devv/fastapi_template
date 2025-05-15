from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated

from db.database import db
from repositories import RepositoryManager


def get_repositories(
        session: Annotated[AsyncSession, Depends(db.session_dependency)]
) -> RepositoryManager:
    return RepositoryManager(session)
