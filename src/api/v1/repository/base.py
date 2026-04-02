from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.base import Base

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    model: type[T]

    def __init__(self, session: AsyncSession, model: type[T]) -> None:
        self.session = session
        self.model = model

    async def by_id(self, id_: str) -> T | None:
        stmt = select(self.model).where(self.model.id == id_).limit(1)
        result = await self.session.execute(stmt)
        return result.scalar()

    async def delete(self, instance: T) -> T:
        instance.is_deleted = True
        await self.session.commit()
        return instance
