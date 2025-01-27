# app/api/v1/endpoints/user_router.py
from typing import List
from fastapi import APIRouter, Depends

from app.domain.user.service import UserService, get_user_service
from app.schemas.user_schema import UserCreate, UserRead

router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"],
)

@router.post("/", response_model=UserRead)
async def create_user(
    user_create: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.create_user(user_create)

@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.get_user(user_id)

@router.get("/", response_model=List[UserRead])
async def list_users(
    skip: int = 0,
    limit: int = 10,
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.get_users(skip=skip, limit=limit)

@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service)
):
    await user_service.delete_user(user_id)
    return
