from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, EmailStr, Field


class Role(str, Enum):
    admin = "admin"
    partner = "partner"
    user = "user"


class User(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Role = Role.user
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
