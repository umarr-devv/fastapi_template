from os import PathLike

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from core.paths import STATIC_DIR, TEMPLATES_DIR


class StaticAssets:
    path: str = '/static'
    name: str = 'static'
    directory: PathLike = STATIC_DIR

    @classmethod
    def mount(cls, app: FastAPI):
        app.mount(cls.path, StaticFiles(directory=cls.directory), name=cls.name)


templates = Jinja2Templates(directory=TEMPLATES_DIR)
