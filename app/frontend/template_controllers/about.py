"""
This module contains the router for the 'about' page.
This is to demonstrate FastAPI rendering HTML templates for an existing page/route.
"""

from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/frontend/templates")


@router.get("/about/", response_class=HTMLResponse, include_in_schema=False)
async def not_found_page_resource(request: Request):
    return templates.TemplateResponse(
        "about.html",
        context={"request": request},
        status_code=status.HTTP_404_NOT_FOUND,
    )
