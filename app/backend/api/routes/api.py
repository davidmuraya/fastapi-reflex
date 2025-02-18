from fastapi import APIRouter

# FastAPI routes for APIs
from app.backend.auth.routes import router as auth_routes
from app.backend.customer.routes import router as customer_routes

# An example of an existing route that renders some HTML
from app.frontend.template_controllers.about import router as about_routes

router = APIRouter()

# Include the routers:
router.include_router(customer_routes)
router.include_router(auth_routes)
router.include_router(about_routes)
