from pydantic import BaseModel, EmailStr
from app.utils.globals import UserRole
from app.core.config import settings


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    username: str
    profile_picture: str = f"/{settings.PROFILE_IMAGE_DIR}/default_pfp.jpg"

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class User(BaseModel):
    id: int
    name: str
    username: str
    email: EmailStr
    profile_image_url: str
    is_superuser: bool
    role: UserRole

    class Config:
        orm_mode: True

class UserUpdate(BaseModel):
    name: str | None = None
    role: UserRole or None = None

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

