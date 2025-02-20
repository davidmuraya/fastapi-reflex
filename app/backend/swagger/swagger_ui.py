from fastapi import APIRouter, Depends, Request, status
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import RedirectResponse

from app.backend.auth.auth import get_current_app_user
from app.backend.auth.models import User

router = APIRouter(prefix="/api")


# Apply the new authentication dependency to the route serving the Swagger UI:
@router.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html(
    request: Request, current_user: User = Depends(get_current_app_user)
):
    # check if the user is authenticated, and redirect to the sign-in page if not:
    if not current_user:
        response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
        return response

    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Customer App API",
        swagger_favicon_url="/static/favicon.ico",
        swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    )
