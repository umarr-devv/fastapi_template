from fastapi import FastAPI
from sqladmin import Admin

from admin.file import FileAdmin
from admin.user import UserAdmin
from db.database import db


class AdminDashboard:
    views = [UserAdmin, FileAdmin]

    @classmethod
    def register(cls, app: FastAPI) -> None:
        admin = Admin(
            app, engine=db.engine, session_maker=db.session_factory
        )
        [admin.add_view(view) for view in cls.views]
