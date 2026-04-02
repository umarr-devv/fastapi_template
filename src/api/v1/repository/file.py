from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from models import File
from services.file import FileService

from .base import BaseRepository


class FileRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, File)

    async def add_file(self, upload_file: UploadFile) -> File:
        saved_file = await FileService.save(upload_file)
        file = File(file_name=saved_file, file_type=upload_file.content_type)
        self.session.add(file)
        await self.session.commit()
        return file
