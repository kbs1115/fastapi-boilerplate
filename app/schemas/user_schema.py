# app/schemas/user_schema.py
from pydantic import EmailStr, Field
from app.base.base_response import BaseResponse
from app.base.base_request import BaseRequest

class UserBase(BaseResponse):
    email: EmailStr
    full_name: str | None = None
    is_admin: bool = False

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserRead(UserBase):
    id: int

class UserLogin(BaseRequest):
    email: EmailStr
    password: str

class TokenResponse(BaseResponse):
    access_token: str
    refresh_token: str
    token_type: str
