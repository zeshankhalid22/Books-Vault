import os
from fastapi import HTTPException, status, Depends, UploadFile
from typing import Annotated
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext
from jose import JWTError, jwt

from app.models import user as UserModel
from app.schemas.user import UserLogin, UserCreate, UserUpdate, Token
from app.core.config import settings
from app.core.dependencies import get_db, oauth2_scheme
from app.utils.globals import UserRole

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(UserModel.User).filter(UserModel.User.email == email))
    return result.scalars().first()


async def get_user_by_id(db: AsyncSession, user_id: int):
    result = await db.execute(select(UserModel.User).filter(UserModel.User.id == user_id))
    db_user = result.scalars().first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


async def create_new_user(db: AsyncSession, user: UserCreate):
    existing_user = await db.execute(
        select(UserModel.User).filter(
            (UserModel.User.email == user.email) | (UserModel.User.username == user.username)
        )
    )
    existing_user = existing_user.scalars().first()
    if existing_user:
        if existing_user.email == user.email:
            raise HTTPException(status_code=400, detail="Email already exists")
        if existing_user.username == user.username:
            raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = pwd_context.hash(user.password)
    new_user = UserModel.User(
        email=str(user.email),
        hashed_password=hashed_password,
        name=user.name,
        username=user.username,
        profile_image_url=user.profile_picture,  # default profile pic from schema
        role=UserRole.USER
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def upload_profile_image(db: AsyncSession, user_id: int, profile_image: UploadFile):
    db_user = await db.execute(select(UserModel.User).filter(UserModel.User.id == user_id))
    db_user = db_user.scalars().first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    profile_image_path = os.path.join(settings.PROFILE_IMAGE_DIR, profile_image.filename)
    with open(profile_image_path, "wb") as image_file:
        image_file.write(await profile_image.read())
    profile_image_url = f"/{settings.PROFILE_IMAGE_DIR}/{profile_image.filename}"

    db_user.profile_image_url = profile_image_url
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def read_all_user(db: AsyncSession, skip: int, limit: int):
    result = await db.execute(select(UserModel.User).offset(skip).limit(limit))
    return result.scalars().all()


async def update_user(db: AsyncSession, user_id: int, user: UserUpdate):
    db_user = await get_user_by_id(db, user_id)
    updated_data = user.model_dump(exclude_unset=True)
    for key, value in updated_data.items():
        setattr(db_user, key, value)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def delete_user(db: AsyncSession, user_id: int):
    db_user = await get_user_by_id(db, user_id)
    await db.delete(db_user)
    await db.commit()
    return {"message": "User deleted successfully"}


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(db: AsyncSession, user: UserLogin):
    member = await get_user_by_email(db, str(user.email))
    if not member:
        return False
    if not verify_password(user.password, member.hashed_password):
        return False
    return member


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.REFRESH_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def refresh_access_token(db: AsyncSession, refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, settings.REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        member = await get_user_by_id(db, int(user_id))
        if member is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"id": member.id, "email": member.email},
            expires_delta=access_token_expires
        )
        return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")


async def verify_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                              db: Annotated[AsyncSession, Depends(get_db)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        current_email: str = payload.get("email")
        if current_email is None:
            raise credentials_exception
        user = await get_user_by_email(db, current_email)
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception
