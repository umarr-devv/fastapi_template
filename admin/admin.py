from sqladmin import Admin
from fastapi import APIRouter, FastAPI
from db.database import db
from admin.file import FileAdmin


def register_admin(app: FastAPI) -> None:
    admin = Admin(
        app, engine=db.engine, session_maker=db.session_factory
    )
    admin.add_view(FileAdmin)
