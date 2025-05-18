from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from core.templates import templates

router = APIRouter(prefix='/home')


@router.get("/", response_class=HTMLResponse)
async def on_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
