from fastapi import APIRouter
from app.api.endpoints.upload_request.upload_request import upload_request_module
from app.api.endpoints.upload_request.upload_request import admin_upload_request_module

upload_request_router = APIRouter()

upload_request_router.include_router(
    upload_request_module,
    prefix="/upload_request",
    tags=["upload_request"],
    responses={404: {"description": "Not found"}},
)

upload_request_router.include_router(
    admin_upload_request_module,
    prefix="/admin/upload_request",
    tags=["admin_upload_request"],
    responses={404: {"description": "Not found"}},
)
