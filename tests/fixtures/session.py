import pytest
from typing_extensions import AsyncGenerator

from core.config import config
from db.database import DataBase
from repositories import RepositoryManager


@pytest.fixture(scope="function")
async def rep_manager() -> AsyncGenerator[RepositoryManager]:
    db = DataBase(config)
    session = db.session_factory()
    try:
        yield RepositoryManager(session)
    finally:
        await session.close()
