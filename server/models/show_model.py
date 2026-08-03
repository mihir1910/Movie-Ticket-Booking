from datetime import datetime, timezone

from pydantic import BaseModel, Field


class Show(BaseModel):
    name: str
    date: datetime
    time: str
    totalSeats: float
    ticketPrice: float
    bookedSeats: list = []
    movie: str
    theatre: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
