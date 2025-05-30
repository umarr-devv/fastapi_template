import uvicorn
from fastapi import FastAPI

from admin import AdminDashboard
from api import router as api_router
from core.cache import RedisCacheConfig
from core.logger import Logging
from core.templates import StaticAssets
from views import router as views_router

Logging.set()
RedisCacheConfig.set()

app = FastAPI()

app.include_router(api_router)
app.include_router(views_router)

AdminDashboard.register(app)
StaticAssets.mount(app)


def main():
    uvicorn.run('app:app', host='0.0.0.0', port=8000, reload=True)


if __name__ == '__main__':
    main()
