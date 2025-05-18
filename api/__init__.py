from fastapi import APIRouter

from api.file import router as file_router
from api.health import router as health_router
from api.user import router as user_router

router = APIRouter(prefix='/api')

router.include_router(file_router)
router.include_router(user_router)
router.include_router(health_router)
