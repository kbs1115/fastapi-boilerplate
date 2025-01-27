# app/routers/auth_router.py
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.config import settings
from app.core.security import (
    create_access_token, 
    create_refresh_token, 
    decode_token
)
from app.database import get_db
from app.models.user import User
from app.schemas.user_schema import UserLogin, TokenResponse
from app.utils.password import verify_password

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Auth"],
)

@router.post("/login", response_model=TokenResponse)
async def login(user_login: UserLogin, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.email == user_login.email)
    result = await db.execute(stmt)
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not verify_password(user_login.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email, "is_admin": user.is_admin},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_refresh_token(
        data={"sub": str(user.id), "email": user.email, "is_admin": user.is_admin},
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_token: str = Header(..., description="Provide Refresh Token in 'refresh_token' header"),
    db: AsyncSession = Depends(get_db)
):
    payload = decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    # 실제 운영에서는 Refresh Token의 유효성을 추가로 검증해야 합니다.
    stmt = select(User).where(User.id == int(payload["sub"]))
    result = await db.execute(stmt)
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    new_access_token = create_access_token(
        data={
            "sub": str(user.id), 
            "email": user.email,
            "is_admin": user.is_admin
        }
    )
    new_refresh_token = create_refresh_token(
        data={
            "sub": str(user.id), 
            "email": user.email,
            "is_admin": user.is_admin
        }
    )

    return TokenResponse(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        token_type="bearer"
    )

@router.post("/logout")
async def logout():
    # 실무에서는 Refresh Token을 블랙리스트에 추가하거나 삭제하는 로직 필요
    return {"message": "Successfully logged out"}
