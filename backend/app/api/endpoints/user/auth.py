from fastapi import APIRouter, Depends, HTTPException, status, Response
from typing import Annotated
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession

# local imports
from app.schemas.user import User, UserLogin, Token
from app.core.dependencies import get_db
from app.core.config import settings
from app.api.endpoints.user import functions as user_functions

auth_module = APIRouter()


# ============> login/logout < ======================
# getting access token for login
@auth_module.post("/login", response_model=Token)
async def login_for_access_token(
        user: UserLogin,
        db: AsyncSession = Depends(get_db)
) -> Token:
    member = await user_functions.authenticate_user(db, user=user)
    if not member:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = user_functions.create_access_token(
        data={"id": member.id, "email": member.email, "role": member.role}, expires_delta=access_token_expires
    )

    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = await user_functions.create_refresh_token(
        data={"id": member.id, "email": member.email, "role": member.role},
        expires_delta=refresh_token_expires
    )
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


@auth_module.post("/refresh", response_model=Token)
async def refresh_access_token(refresh_token: str, db: AsyncSession = Depends(get_db)):
    token = await user_functions.refresh_access_token(db, refresh_token)
    return token

# get current user
@auth_module.get('/users/me/', response_model=User)
async def get_current_user(current_user: Annotated[User, Depends(user_functions.verify_current_user)]):
    return current_user

# Endpoint to varify only the token
@auth_module.get("/verify-token")
async def verify_token(current_user: User = Depends(user_functions.verify_current_user)):
    # Just return a minimal response - the dependency already validates the token
    return {"valid": True}

@auth_module.post("/logout")
async def logout(
    response: Response,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(user_functions.verify_current_user)
):

    # call logout function and return
    result = {"message": "Successfully logged out"}

    # Clear the HTTP-only cookies that contain the tokens
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")

    return result
