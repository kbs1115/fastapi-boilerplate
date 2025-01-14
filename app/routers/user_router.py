# app/routers/user_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserRead
from app.utils.password import hash_password

router = APIRouter()

@router.post("/", response_model=UserRead)
async def create_user(user_create: UserCreate, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.email == user_create.email)
    result = await db.execute(stmt)
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    new_user = User(
        email=user_create.email,
        hashed_password=hash_password(user_create.password),
        full_name=user_create.full_name,
        is_admin=user_create.is_admin
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user

@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
