from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from app.models.user import UserRole


class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=255)
    student_id: Optional[str] = Field(None, max_length=50)
    major: Optional[str] = Field(None, max_length=100)
    class_year: Optional[str] = Field(None, max_length=20)


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=72, description="Password must be between 8 and 72 characters (bcrypt limitation)")


class UserResponse(UserBase):
    id: int
    role: UserRole
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class User(UserResponse):
    pass

