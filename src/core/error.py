import logging

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exception_handlers import http_exception_handler


class ErrorHandler:

    @classmethod
    def set(cls, app: FastAPI):
        @app.exception_handler(HTTPException)
        async def logging_http_exception_handler(request: Request, exc: HTTPException):
            if exc.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
                logging.critical(exc)
            else:
                logging.error(exc)
            return await http_exception_handler(request, exc)
