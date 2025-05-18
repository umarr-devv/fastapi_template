from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from core.paths import STATIC_DIR, TEMPLATES_DIR


def mount_static(app: FastAPI):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


templates = Jinja2Templates(directory=TEMPLATES_DIR)
