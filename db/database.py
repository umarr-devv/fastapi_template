from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from typing_extensions import AsyncGenerator

from core.config import ConfigModel


class DataBase:

    def __init__(self, config: ConfigModel) -> None:
        self.engine = create_async_engine(
            url=config.database_url
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    @asynccontextmanager
    async def session_dependency(self) -> AsyncGenerator[AsyncSession]:
        async with self.session_factory() as session:
            yield session
            await session.close()
