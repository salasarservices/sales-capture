from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime


class UserRole(str, Enum):
    admin = "admin"
    viewer = "viewer"


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    role: UserRole = UserRole.viewer

    model_config = {"use_enum_values": True}


class UserOut(BaseModel):
    id: str = Field(alias="_id")
    username: str
    role: str
    created_at: Optional[datetime] = None

    model_config = {"populate_by_name": True}


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    username: str
    password: str
