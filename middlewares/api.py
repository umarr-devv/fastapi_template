import logging

from fastapi.requests import Request
from fastapi.responses import Response, JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class CustomAPIMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next) -> Response:
        try:
            response: Response = await call_next(request)
            return response
        except Exception as exc:
            logging.error(exc)
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal Server Error"},
            )
