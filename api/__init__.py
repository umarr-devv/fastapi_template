from fastapi import APIRouter
from api.file import router as file_router

router = APIRouter(prefix='/api')
router.include_router(file_router)
