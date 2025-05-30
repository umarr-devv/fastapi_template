from pathlib import Path
from uuid import uuid4

import aiofiles
from fastapi import UploadFile

from core.paths import FILE_DIR


class FileService:

    @staticmethod
    async def save(file: UploadFile) -> str:
        unique_file_name = f'{uuid4().hex}_{file.filename}'
        file_path = FileService.get(unique_file_name)

        async with aiofiles.open(file_path, mode='wb') as file_:
            content = await file.read()
            await file_.write(content)
        return unique_file_name

    @staticmethod
    def get(unique_file_name: str) -> Path:
        return FILE_DIR / unique_file_name
