import pytest
from typing_extensions import AsyncGenerator

from core.config import config
from db.database import DataBase
from src.api.v1.repository import RepositoriesManager


@pytest.fixture(scope="function")
async def rep_manager() -> AsyncGenerator[RepositoriesManager]:
    db = DataBase(config)
    session = db.session_factory()
    try:
        yield RepositoriesManager(session)
    finally:
        await session.close()
