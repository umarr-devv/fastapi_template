from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Generic, TypeVar, Optional, Sequence

from db.base import Base

T = TypeVar('T', bound=Base)


class BaseRepository(Generic[T]):
    model: type[T]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def by_id(self, obj_id: int) -> Optional[T]:
        statement = select(self.model).where(self.model.id == obj_id)
        result = await self.session.execute(statement)
        return result.scalar()

    async def by_filter_one(self, **kwargs) -> Optional[T]:
        statement = select(self.model).filter_by(**kwargs).limit(1)
        result = await self.session.execute(statement)
        return result.scalar()

    async def all(self) -> Sequence[T]:
        statement = select(self.model).order_by(self.model.create_at)
        result = await self.session.execute(statement)
        return result.unique().scalars().all()

    async def new(self, **kwargs) -> T:
        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.flush()
        return instance
