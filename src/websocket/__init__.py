from fastapi import APIRouter

from websocket.default import router as default_router

router = APIRouter(prefix='/ws')
router.include_router(default_router)
