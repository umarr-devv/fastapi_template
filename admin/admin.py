from fastapi import FastAPI
from sqladmin import Admin, ModelView

from admin.auth import AdminAuth
from admin.views.file import FileAdmin
from admin.views.user import UserAdmin
from core.config import config
from db.database import db


class AdminDashboard:
    views: list[type[ModelView]] = [UserAdmin, FileAdmin]

    @classmethod
    def register(cls, app: FastAPI) -> None:
        admin = Admin(
            app,
            engine=db.engine,
            session_maker=db.session_factory,
            authentication_backend=AdminAuth(config.app.secret_key),
        )
        [admin.add_view(view) for view in cls.views]
