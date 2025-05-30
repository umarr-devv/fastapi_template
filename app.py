import uvicorn
from fastapi import FastAPI

from admin import register_admin
from api import router as api_router
from core.config import config
from core.logger import set_logging
from core.templates import mount_static
from views import router as views_router
from core.cache import RedisCacheConfig

app = FastAPI()

set_logging(config)
register_admin(app)
mount_static(app)

app.include_router(api_router)
app.include_router(views_router)

RedisCacheConfig.set()


def main():
    uvicorn.run('app:app', host='0.0.0.0', port=8000, reload=True)


if __name__ == '__main__':
    main()
