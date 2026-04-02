from sqlalchemy.ext.asyncio import AsyncSession

from .file import FileRepository
from .user import UserRepository


class RepositoriesManager:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.files = FileRepository(session)
        self.users = UserRepository(session)

    async def commit(self):
        await self.session.commit()
