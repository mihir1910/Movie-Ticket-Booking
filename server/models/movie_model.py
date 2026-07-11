from datetime import datetime, timezone

from pydantic import BaseModel, Field


class Movie(BaseModel):
    title: str
    description: str | None = None
    language: str
    posterPath: str
    genre: str
    releaseDate: datetime
    duration: float
    ratings: float | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
