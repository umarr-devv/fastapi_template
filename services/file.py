from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

FILE_DIR = Path('files')
FILE_DIR.mkdir(parents=True, exist_ok=True)


class FileService:

    @staticmethod
    async def save(file: UploadFile) -> str:
        unique_file_name = f'{uuid4().hex}_{file.filename}'

        with open(FileService.get(unique_file_name), mode='wb') as f:
            f.write(await file.read())
        return unique_file_name

    @staticmethod
    def get(unique_file_name: str) -> Path:
        return FILE_DIR / unique_file_name
