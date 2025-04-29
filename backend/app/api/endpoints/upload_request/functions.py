from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.upload_request import UploadRequestCreate
from app.models.upload_request import UploadRequest
from app.models.content import Content

async def create_upload_request(db: AsyncSession, request_data: UploadRequestCreate, user_id: int):
    """Allow users to submit a new upload request"""
    new_request = UploadRequest(
        title=request_data.title,
        author=request_data.author,
        type=request_data.type,
        genre=request_data.genre,
        rating=request_data.rating,
        cover_image=request_data.cover_image,
        abstract=request_data.abstract,
        requested_by=user_id
    )
    db.add(new_request)
    await db.commit()
    await db.refresh(new_request)
    return new_request

async def get_user_requests(db: AsyncSession, user_id: int):
    """Get all upload requests submitted by a specific user"""
    result = await db.execute(
        select(UploadRequest).where(UploadRequest.requested_by == user_id)
    )
    return result.scalars().all()

# --- Admin functions

async def get_request_by_id(db: AsyncSession, request_id: int):
    result = await db.execute(
        select(UploadRequest).where(UploadRequest.id == request_id)
    )
    return result.scalars().first()

async def get_all_pending_requests(db: AsyncSession):
    result = await db.execute(
        select(UploadRequest).where(UploadRequest.status == "pending")
    )
    return result.scalars().all()

async def approve_request(db: AsyncSession, request_id: int):
    # Get the request
    result = await db.execute(
        select(UploadRequest).where(UploadRequest.id == request_id)
    )
    request = result.scalars().first()

    if not request or request.status != "pending":
        return None

    # Update status
    request.status = "approved"

    # Create content record
    content = Content(**request.to_content_dict())
    db.add(content)
    await db.flush()  # Get ID without committing

    # Create book or article based on type
    if request.type == "book":
        model = request.build_book(content.id)
    else:
        model = request.build_article(content.id)

    db.add(model)
    await db.commit()
    await db.refresh(request)
    return request

async def reject_request(db: AsyncSession, request_id: int):
    """Reject a pending upload request - admin only function"""
    request = await get_request_by_id(db, request_id)
    if not request or request.status != "pending":
        return None

    request.status = "rejected"
    await db.commit()
    await db.refresh(request)
    return request