from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db, get_current_user, admin_role_check
from app.schemas.upload_request import UploadRequestCreate, UploadRequestResponse
from app.schemas.user import User
from . import functions

upload_request_module = APIRouter()
admin_upload_request_module =APIRouter()

# User endpoints
@upload_request_module.post("/", response_model=UploadRequestResponse)
async def create_request(
        request: UploadRequestCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Allow any authenticated user to create an upload request"""
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Authentication required"
        )

    return await functions.create_upload_request(db, request, current_user.id)


@upload_request_module.get("/my", response_model=list[UploadRequestResponse])
async def get_my_requests(
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Get all requests submitted by the current user"""
    return await functions.get_user_requests(db, current_user.id)

# --- Admin endpoints

@admin_upload_request_module.get("/{request_id}", response_model=UploadRequestResponse)
async def get_request(
        request_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Get a specific request by ID"""
    request = await functions.get_request_by_id(db, request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    # Only allow user to view their own requests unless they're an admin
    if request.requested_by != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to view this request")

    return request


@admin_upload_request_module.get("/pending", response_model=list[UploadRequestResponse])
async def get_all_pending_requests(
        db: AsyncSession = Depends(get_db),
        _: User = Depends(admin_role_check)  # Only admins can access
):
    return await functions.get_all_pending_requests(db)


@admin_upload_request_module.post("/{request_id}/approve", response_model=UploadRequestResponse)
async def approve_upload_request(
        request_id: int,
        db: AsyncSession = Depends(get_db),
        _: User = Depends(admin_role_check)  # Only admins can access
):
    result = await functions.approve_request(db, request_id)
    if not result:
        raise HTTPException(status_code=404, detail="Request not found or already processed")
    return result


@admin_upload_request_module.post("/{request_id}/reject", response_model=UploadRequestResponse)
async def reject_upload_request(
        request_id: int,
        db: AsyncSession = Depends(get_db),
        _: User = Depends(admin_role_check)  # Only admins can access
):
    result = await functions.reject_request(db, request_id)
    if not result:
        raise HTTPException(status_code=404, detail="Request not found or already processed")
    return result
