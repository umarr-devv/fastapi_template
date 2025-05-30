from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from typing_extensions import AsyncGenerator

from core.config import ConfigModel, config


class DataBase:

    def __init__(self, config: ConfigModel) -> None:
        self.engine = create_async_engine(
            url=config.database.url
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def session_dependency(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session
            await session.close()


db = DataBase(config)
