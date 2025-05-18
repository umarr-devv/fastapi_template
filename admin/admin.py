from fastapi import FastAPI
from sqladmin import Admin

from admin.file import FileAdmin
from admin.user import UserAdmin
from db.database import db


def register_admin(app: FastAPI) -> None:
    admin = Admin(
        app, engine=db.engine, session_maker=db.session_factory
    )
    admin.add_view(FileAdmin)
    admin.add_view(UserAdmin)
