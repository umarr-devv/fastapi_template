from fastapi import Request
from sqladmin.authentication import AuthenticationBackend

from core.config import config


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        if username == config.admin.username and password == config.admin.password:
            request.session.update({"sub": username})
            return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        return request.session.get("sub") == config.admin.username
