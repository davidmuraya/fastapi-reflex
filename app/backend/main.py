from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.backend.api.routes.api import router as api_router
from app.backend.database.utils import initialize_database

app = FastAPI(on_startup=[initialize_database])

templates = Jinja2Templates(directory="app/frontend/customer_app/.web/_static")


# Mount the "/static" directory for serving static files such as CSS, JavaScript, and images
app.mount(
    "/_next",
    StaticFiles(directory="app/frontend/customer_app/.web/_static/_next"),
    name="_next",
)

# Include the defined API routers into the application
app.include_router(api_router)


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def index_page_resource(request: Request):
    context = {
        "request": request,
    }

    return templates.TemplateResponse("index.html", context=context)
