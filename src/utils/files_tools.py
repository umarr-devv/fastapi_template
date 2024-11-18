import os
import uuid

from fastapi import UploadFile

FILE_DIR = os.getcwd() + '/files'


async def save_file(file: UploadFile) -> tuple[str]:
    unique_filename = f'{uuid.uuid4().hex}_{file.filename}'
    with open(f'{FILE_DIR}/{unique_filename}', mode='wb') as f:
        f.write(await file.read())
    return file.filename, unique_filename
