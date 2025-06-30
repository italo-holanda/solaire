from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field


class Entity(BaseModel):
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))

    deleted_at: Optional[datetime] = None
