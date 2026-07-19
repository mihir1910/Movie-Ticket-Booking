from datetime import datetime, timezone

from pydantic import BaseModel, Field


class Theatre(BaseModel):
    name: str
    address: str
    email: str
    phone: float
    isActive: bool = False
    owner: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
