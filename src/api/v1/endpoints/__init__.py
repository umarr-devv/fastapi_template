from fastapi import APIRouter

from .file import router as file_router
from .health import router as health_router
from .user import router as user_router

router = APIRouter(prefix="/v1", tags=["v1"])
router.include_router(file_router)
router.include_router(user_router)
router.include_router(health_router)
