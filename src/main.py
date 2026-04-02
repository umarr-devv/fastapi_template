import uvicorn
from fastapi import FastAPI

from api import router as api_router
from core.cache import CacheConfig
from core.error import ErrorHandler
from core.logger import Logging
from middlewares import *
from websocket import router as websocket_router

app = FastAPI()
app.include_router(api_router)
app.include_router(websocket_router)
app.add_middleware(CustomCorsMiddleware)

Logging.set()
CacheConfig.set()
ErrorHandler.set(app)


def main():
    uvicorn.run("main:app", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
