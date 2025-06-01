import uvicorn
from fastapi import FastAPI

from admin import AdminDashboard
from api import router as api_router
from core.cache import RedisCacheConfig
from core.error import ErrorHandler
from core.lifespan import lifespan
from core.logger import Logging
from core.templates import StaticAssets
from middlewares import CustomCorsMiddleware, CustomAPIMiddleware
from websocket import router as socket_router
from views import router as views_router

Logging.set()
RedisCacheConfig.set()

app = FastAPI(lifespan=lifespan)

app.add_middleware(CustomCorsMiddleware)
app.add_middleware(CustomAPIMiddleware)

app.include_router(api_router)
app.include_router(views_router)
app.include_router(socket_router)

AdminDashboard.register(app)
StaticAssets.mount(app)

ErrorHandler.set(app)


def main():
    uvicorn.run('app:app', host='0.0.0.0', port=8000, reload=True)


if __name__ == '__main__':
    main()
