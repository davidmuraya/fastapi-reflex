from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware

from app.backend.api.routes.api import router as api_router
from app.backend.database.utils import initialize_database
from app.backend.middleware.log_middleware import log_and_track_request_process_time
from app.backend.middleware.security_headers import add_security_headers

origins = [
    "https://demo.bima-mo.com",
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
]

# Create a FastAPI application instance.
# The 'on_startup' parameter ensures that 'initialize_database' is called when the app starts.
app = FastAPI(on_startup=[initialize_database])


# Include the API router in the application.
# This will mount all API endpoints defined in 'api_router'.
app.include_router(api_router)


# Define a subclass of StaticFiles to create a custom static file handler
# that supports client-side routing in Single Page Applications (SPAs).
class SPAStaticFiles(StaticFiles):
    # Override the get_response method, which is responsible for retrieving
    # static file responses for given paths.
    async def get_response(self, path: str, scope):
        try:
            return await super().get_response(path, scope)
        except (HTTPException, StarletteHTTPException) as ex:
            if ex.status_code == 404:
                return await super().get_response("index.html", scope)
            else:
                raise ex


# Mount the SPAStaticFiles instance at the root URL ("/").
# This means any request not caught by other routes (like the API) will be handled here.
# - 'directory' specifies where your built static files (from Next.js) reside.
# - 'html=True' tells FastAPI to serve HTML files by default.
# - 'name' is an identifier for this mounted application
app.mount(
    "/",
    SPAStaticFiles(directory="app/frontend/customer_app/.web/_static/", html=True),
    name="_next",
)

# Add middleware to the application to add security headers to responses:
app.add_middleware(BaseHTTPMiddleware, dispatch=add_security_headers)


# Add middleware to the application to add process time header to responses:
app.add_middleware(BaseHTTPMiddleware, dispatch=log_and_track_request_process_time)

# CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
