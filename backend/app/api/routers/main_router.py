from fastapi import APIRouter

from app.api.endpoints.upload_request.upload_request import admin_upload_request_module
from app.api.routers.user import user_router
from app.api.routers.book import book_router
from app.api.routers.upload_request import upload_request_router

router = APIRouter()

router.include_router(user_router)
router.include_router(book_router)
router.include_router(upload_request_router)
router.include_router(admin_upload_request_module)


