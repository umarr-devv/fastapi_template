from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from src.config import Config, config


class Base(DeclarativeBase):
    __abstract__ = True


class DataBase:

    def __init__(self, _config: Config):
        self.engine = create_async_engine(
            url=_config.db.url
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False
        )

    async def session_dependency(self) -> AsyncSession:
        async with self.session_factory() as session:
            yield session
            await session.close()


db = DataBase(config)
