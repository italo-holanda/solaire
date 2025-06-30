from abc import ABC, abstractmethod

from backend.core.domain.entities.thought import Thought


class ThoughtVectorStore(ABC):
    @abstractmethod
    def create_index(thought: Thought) -> None:
        pass
