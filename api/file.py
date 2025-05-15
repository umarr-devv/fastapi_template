from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File as FastAPIFile
from fastapi.responses import FileResponse
from typing_extensions import Annotated

from deps import get_repositories
from repositories import RepositoryManager
from schemes import FileScheme
from services.file import FileService

router = APIRouter(prefix='/files', tags=['files'])


@router.post(
    path='',
    response_model=FileScheme
)
async def on_create_file(
        file: Annotated[UploadFile, FastAPIFile(...)],
        rep_manager: Annotated[RepositoryManager, Depends(get_repositories)]
):
    file_name = await FileService.save(file)
    file = await rep_manager.file.new(file_name=file_name, file_type=file.content_type)
    await rep_manager.commit()
    return file


@router.get(
    path='/{file_id}',
    response_class=FileResponse
)
async def on_get_file(
        file_id: int,
        rep_manager: Annotated[RepositoryManager, Depends(get_repositories)]
):
    file = await rep_manager.file.by_id(file_id)

    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='file not found'
        )
    return FileResponse(
        path=FileService.get(file.file_name)
    )
