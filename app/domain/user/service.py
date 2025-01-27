# app/services/user_service.py
from typing import Optional, List
from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.domain.user.repository import UserRepository
from app.base.base_service import BaseService
from app.schemas.user_schema import UserCreate, UserRead
from app.utils.password import hash_password


class UserService(BaseService):
    def __init__(self, db: AsyncSession):
        self.user_repository = UserRepository(db)
        super().__init__(db)

    async def create_user(self, user_create: UserCreate) -> UserRead:
        existing_user = await self.user_repository.get_by_email(user_create.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        hashed_pwd = hash_password(user_create.password)
        new_user = await self.user_repository.create(user_create, hashed_pwd)
        return UserRead.model_validate(new_user)

    async def get_user(self, user_id: int) -> UserRead:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return UserRead.model_validate(user)

    async def get_users(self, skip: int = 0, limit: int = 10) -> List[UserRead]:
        users = await self.user_repository.get_all(skip=skip, limit=limit)
        return [UserRead.model_validate(user) for user in users]

    async def delete_user(self, user_id: int) -> None:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        await self.user_repository.delete(user_id)


# Dependency for UserService
def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)