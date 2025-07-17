import logging

from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File as FastAPIFile, Path
from fastapi.responses import FileResponse
from typing_extensions import Annotated

from deps import get_rep_manager
from models import File
from repositories import RepositoryManager
from schemes import FileScheme
from services.file import FileService

router = APIRouter(prefix='/files', tags=['files'])


@router.post(
    path='',
    response_model=FileScheme
)
async def on_create_file(
        upload_file: Annotated[UploadFile, FastAPIFile(...)],
        rep_manager: Annotated[RepositoryManager, Depends(get_rep_manager)]
):
    try:
        file_name = await FileService.save(upload_file)

        file = File(file_name=file_name, file_type=upload_file.content_type)
        await rep_manager.add(file)
        await rep_manager.commit()
        return file
    except Exception as exc:
        logging.error(exc)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )


@router.get(
    path='/{file_id}',
    response_class=FileResponse
)
async def on_get_file(
        file_id: Annotated[int, Path(...)],
        rep_manager: Annotated[RepositoryManager, Depends(get_rep_manager)]
):
    file = await rep_manager.by_id(File, id_=file_id)

    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='file not found'
        )
    return FileResponse(
        path=FileService.get(file.file_name)
    )
