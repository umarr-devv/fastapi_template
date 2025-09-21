from typing import Any

from sqlalchemy import Result, Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.elements import ColumnElement
from typing_extensions import Sequence, TypeVar

from db.base import Base

T = TypeVar("T", bound=Base)


class RepositoryManager:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def refresh(self, instance: T) -> T | None:
        return await self.by_id(model=type(instance), id_=instance.id)

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def execute(self, stmt: Select) -> Result:
        return await self.session.execute(stmt)

    async def by_id(self, model: type[T], id_: str | Mapped[int]) -> T | None:
        stmt = select(model).where(model.id == id_).limit(1)
        result = await self.session.execute(stmt)
        return result.scalar()

    async def by_condition_one(
        self,
        model: type[T],
        *conditions: Any,
    ) -> T | None:
        stmt = select(model).where(*conditions)
        result = await self.session.execute(stmt)
        return result.scalar()

    async def by_condition_all(
        self,
        model: type[T],
        *conditions: Any,
        limit: int | None = None,
        offset: int = 0,
        order_by: ColumnElement | None = None,
    ) -> Sequence[T]:
        stmt = (
            select(model)
            .where(*conditions)
            .limit(limit)
            .offset(offset)
            .order_by(order_by)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def count_by_conditions(self, model: type[T], *conditions: Any) -> int:
        stmt = select(func.count(model.id)).where(*conditions)
        result = await self.session.execute(stmt)
        return result.scalar() or 0

    async def paginate(
        self,
        model: type[T],
        *conditions: Any,
        limit: int | None = None,
        offset: int = 0,
        order_by: ColumnElement,
    ) -> tuple[Sequence[T], int]:
        items = await self.by_condition_all(
            model=model,
            *conditions,
            limit=limit,
            offset=offset,
            order_by=order_by,
        )
        count = await self.count_by_conditions(
            model=model,
            *conditions,
        )
        return items, count

    async def add(self, instance: T) -> T:
        self.session.add(instance)
        await self.session.flush([instance])
        return instance

    async def add_all(self, instances: list[T]) -> list[T]:
        self.session.add_all(instances)
        await self.session.flush(instances)
        return instances
