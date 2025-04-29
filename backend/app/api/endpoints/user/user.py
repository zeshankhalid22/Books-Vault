from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db, admin_role_check
from app.schemas.user import User, UserCreate, UserUpdate
from app.api.endpoints.user import functions as user_functions

user_module = APIRouter()

@user_module.post('/', response_model=User)
async def create_new_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    return await user_functions.create_new_user(db, user)

@user_module.get('/', response_model=list[User])
async def read_all_user(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await user_functions.read_all_user(db, skip, limit)


@user_module.post('/upload-profile-image', response_model=User)
async def upload_profile_image_endpoint(
    user_id: int,
    profile_image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    return await user_functions.upload_profile_image(db, user_id, profile_image)

@user_module.get('/{user_id}', response_model=User)
async def read_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    return await user_functions.get_user_by_id(db, user_id)

@user_module.patch('/{user_id}', response_model=User)
async def update_user(user_id: int, user: UserUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(admin_role_check)):
    if user.role and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Only admins can update the role")
    return await user_functions.update_user(db, user_id, user)

@user_module.delete('/{user_id}')
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await user_functions.delete_user(db, user_id)