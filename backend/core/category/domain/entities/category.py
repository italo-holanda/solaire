from typing import Optional
from backend.core.common.domain.entities.entity import Entity
from backend.core.common.domain.util.remove_extra_spaces import generate_random_color
from pydantic import Field


class Category(Entity):
    name: str
    color: Optional[str] = Field(default_factory=generate_random_color)
