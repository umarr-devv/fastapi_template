from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.elements import ColumnElement
from typing_extensions import Sequence, TypeVar

from db.base import Base

T = TypeVar('T', bound=Base)


class RepositoryManager:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def by_id(self, model: type[T], id_: int | Mapped[int]) -> T | None:
        stmt = select(model).where(model.id == id_).limit(1)
        result = await self.session.execute(stmt)
        return result.scalar()

    async def by_condition_one(
            self, model: type[T],
            *conditions: bool | ColumnElement[bool],
    ) -> T | None:
        stmt = select(model).where(*conditions)
        result = await self.session.execute(stmt)
        return result.scalar()

    async def by_condition_all(
            self, model: type[T],
            *conditions: bool | ColumnElement[bool],
            limit: int | None = None,
            offset: int = 0
    ) -> Sequence[T]:
        stmt = select(model).where(*conditions).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def add(self, instance: T) -> T:
        self.session.add(instance)
        await self.session.flush([instance])
        return instance

    async def add_all(self, instances: list[T]) -> list[T]:
        self.session.add_all(instances)
        await self.session.flush(instances)
        return instances

    async def refresh(self, instance: T) -> T:
        return await self.by_id(
            model=type(instance),
            id_=instance.id
        )

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
