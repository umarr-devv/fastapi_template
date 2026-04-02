from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.schemas import *
from models import *
from services.hash import HashService

from .base import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User)

    async def get_users(self) -> Sequence[User]:
        stmt = select(User).where(User.is_deleted == False)
        result = await self.session.execute(stmt)
        users = result.scalars().all()
        return users

    async def by_username(self, username: str) -> User | None:
        stmt = (
            select(User)
            .where(User.username == username and User.is_deleted == False)
            .limit(1)
        )
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        return user

    async def create_user(self, data: CreateUserSchema) -> User:
        update_data = data.model_copy(
            update={"password": HashService.to_hash(data.password)}
        )
        user = User(**update_data.model_dump())
        self.session.add(user)
        await self.session.commit()
        return user

    async def patch_user(self, instance: User, data: PatchUserSchema) -> User:
        for j, k in data.model_dump(exclude_unset=True).items():
            if hasattr(instance, j):
                setattr(instance, j, k)
        await self.session.commit()
        return instance

    async def patch_user_password(
        self, instance: User, data: PatchUserPasswordSchema
    ) -> User:
        instance.password = HashService.to_hash(data.password)
        await self.session.commit()
        return instance
