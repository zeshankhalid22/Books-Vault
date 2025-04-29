from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db, admin_role_check
from app.schemas.user import User
from app.api.endpoints.user import functions as user_functions

admin_module = APIRouter()

@admin_module.get('/users', response_model=list[User])
async def read_all_users(db: AsyncSession = Depends(get_db), current_user: User = Depends(admin_role_check), skip: int = 0, limit: int = 10):
    return await user_functions.read_all_user(db, skip=skip, limit=limit)