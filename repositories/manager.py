from sqlalchemy.ext.asyncio import AsyncSession

from repositories.file import FileRepository
from repositories.user import UserRepository


class RepositoryManager:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.file = FileRepository(session=session)
        self.user = UserRepository(session=session)

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
