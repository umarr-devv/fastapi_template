import logging

from fastapi import FastAPI, Request, status
from starlette.exceptions import HTTPException as StarletteHTTPException


class ErrorHandler:

    @classmethod
    def set(cls, app: FastAPI):
        @app.exception_handler(StarletteHTTPException)
        async def http_exception_handler(request: Request, exc: StarletteHTTPException):
            if exc.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
                logging.critical(exc)
            return None
