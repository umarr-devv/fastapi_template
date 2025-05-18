from fastapi import APIRouter

from views.home import router as home_router

router = APIRouter(prefix='')
router.include_router(home_router)
