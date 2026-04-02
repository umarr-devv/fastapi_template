from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi import File as FastAPIFile
from fastapi import HTTPException, Path, UploadFile, status
from fastapi.responses import FileResponse

from api.v1.dependencies import *
from api.v1.repository import *
from api.v1.schemas import *
from core.logger import logging
from services import *

router = APIRouter(prefix="/files", tags=["files"])


@router.post(path="/upload", response_model=FileSchema, operation_id="upload_file")
async def on_create_file(
    upload_file: Annotated[UploadFile, FastAPIFile(...)],
    manager: Annotated[RepositoriesManager, Depends(get_manager)],
):
    try:
        return await manager.files.add_file(upload_file)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.get(path="/{file_id}", response_class=FileResponse, operation_id="get_file")
async def on_get_file(
    file_id: Annotated[str, Path()],
    manager: Annotated[RepositoriesManager, Depends(get_manager)],
):
    file = await manager.files.by_id(file_id)

    if file:
        return FileResponse(FileService.get(file.file_name))
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="file not found")
