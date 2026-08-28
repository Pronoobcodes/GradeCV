from datetime import datetime
from pydantic import BaseModel, EmailStr, field_validator, Field
from typing import Optional


class UserCreate(BaseModel):
    full_name: Optional[str] = None
    email: EmailStr
    password: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "full_name": "John Doe",
                "email": "johndoe@example.com",
                "password": "[PASSWORD]",
            }
        }
    }

    @field_validator("password")
    @classmethod
    def prevent_placeholder_password(cls, v: str) -> str:
        # Check for exact match or case-insensitive variation
        if v.strip() == "[PASSWORD]":
            raise ValueError(
                "You cannot use the placeholder '[PASSWORD]' as your actual password."
            )
        return v
    

class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "full_name": "Jane Doe",
            }
        }
    }


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)


class PasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)

    