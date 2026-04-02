from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated

from db.database import db


def get_session(
    session: Annotated[AsyncSession, Depends(db.session_dependency)],
) -> AsyncSession:
    return session
