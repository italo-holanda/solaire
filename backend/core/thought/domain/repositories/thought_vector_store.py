from abc import ABC, abstractmethod
from typing import List

from pydantic import BaseModel

from backend.core.thought.domain.entities.thought import Thought


class ThoughtVector(BaseModel):
    thought_id: str
    embeddings: List[float]


class ThoughtVectorStoreInterface(ABC):
    @abstractmethod
    def create_index(self, thought: Thought) -> None:
        pass

    @abstractmethod
    def search_similar(self, thought: Thought) -> List[ThoughtVector]:
        pass

    @abstractmethod
    def search_similar_by_text(self, thought_text: str) -> List[ThoughtVector]:
        pass

    @abstractmethod
    def delete_index(self, thought: Thought) -> None:
        pass