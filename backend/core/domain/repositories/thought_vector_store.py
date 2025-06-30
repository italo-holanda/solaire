from abc import ABC, abstractmethod
from typing import List

from pydantic import BaseModel

from backend.core.domain.entities.thought import Thought


class ThoughtVector(BaseModel):
    thought_id: str
    embeddings: List[float]


class ThoughtVectorStore(ABC):
    @abstractmethod
    def create_index(thought: Thought) -> None:
        pass

    @abstractmethod
    def search_similar(thought: Thought) -> List[ThoughtVector]:
        pass
