import uvicorn
from fastapi import FastAPI

from admin import register_admin
from api import router

app = FastAPI()

register_admin(app)
app.include_router(router)


def main():
    uvicorn.run('app:app', host='0.0.0.0', port=8000, reload=True)


if __name__ == '__main__':
    main()
