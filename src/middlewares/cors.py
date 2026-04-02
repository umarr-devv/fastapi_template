from typing import Any

from fastapi.middleware.cors import CORSMiddleware
from starlette.types import ASGIApp


class CustomCorsMiddleware(CORSMiddleware):

    def __init__(self, app: ASGIApp, *args: Any, **kwargs: Any) -> None:
        super().__init__(
            app,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
            *args,
            **kwargs
        )
