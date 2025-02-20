from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.gzip import GZipMiddleware

from app.backend.api.routes.api import router as api_router
from app.backend.auth.auth import get_current_app_user
from app.backend.auth.models import User
from app.backend.database.utils import initialize_database
from app.backend.middleware.log_middleware import log_and_track_request_process_time
from app.backend.middleware.security_headers import add_security_headers

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8001",
]

api_description = """
FastAPI + Reflex Application

"""

# Create a FastAPI application instance.
# The 'on_startup' parameter ensures that 'initialize_database' is called when the app starts.
app = FastAPI(
    on_startup=[initialize_database],
    redoc_url=None,
    openapi_url=None,
    docs_url=None,
    title="Customer Data App",
    description=api_description,
    version="1.0.0",
)


# Include the API router in the application.
# This will mount all API endpoints defined in 'api_router'.
app.include_router(api_router)


@app.get("/openapi.json", include_in_schema=False)
async def custom_openapi_json(current_user: User = Depends(get_current_app_user)):
    """
    Blocks access to the OpenAPI JSON endpoint for authenticated users by redirecting them to the sign-in page.

    Args:
        current_user (User, optional): The current authenticated user. Defaults to Depends(get_current_app_user).

    Returns:
        RedirectResponse: Redirects authenticated users to the sign-in page. Returns the OpenAPI JSON data for
        non-authenticated users.

    Note:
        This function prevents authenticated users from accessing the OpenAPI JSON endpoint, enhancing security
        by restricting access to API documentation for unauthorized users.
    """

    if not current_user:
        response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
        return response

    return get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )


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


# Add GZipMiddleware as the last middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)
