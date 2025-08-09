from typing import List
from backend.core.category.domain.entities.category import Category
from backend.core.common.domain.entities.entity import Entity
from backend.core.common.domain.util import remove_extra_spaces
from pydantic import field_validator


class Thought(Entity):
    model_config = {
        "validate_assignment": True
    }
    title: str
    summary: str
    text: str
    categories: List[Category]
    embeddings: List[float]

    @field_validator('text')
    @classmethod
    def validate_text_length(cls, v):
        normalized = remove_extra_spaces(v)
        if len(normalized) < 100 or len(normalized) > 1000:
            raise ValueError('Text must be >= 100 and <= 1000')
        return v