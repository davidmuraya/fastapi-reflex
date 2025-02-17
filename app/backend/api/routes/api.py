from fastapi import APIRouter

from app.backend.auth.routes import router as auth_routes
from app.backend.customer.routes import router as customer_routes

router = APIRouter()


router.include_router(customer_routes)
router.include_router(auth_routes)
