from typing import List
from backend.core.domain.entities.entity import Entity


class Thought(Entity):
    id: str
    title: str
    summary: str
    text: str
    categories: List[str]
    embeddings: List[float]