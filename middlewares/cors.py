from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


class CustomCorsMiddleware(CORSMiddleware):

    def __init__(self, app: FastAPI, *args, **kwargs):
        super().__init__(
            app,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
            *args, **kwargs
        )
