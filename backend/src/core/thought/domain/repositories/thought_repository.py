from abc import ABC, abstractmethod
from typing import List

from src.core.thought.domain.entities.thought import Thought


class ThoughtRepositoryInterface(ABC):

    @abstractmethod
    def save(self, thought: Thought) -> None:
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> Thought:
        pass

    @abstractmethod
    def list(self) -> List[Thought]:
        pass

    @abstractmethod
    def delete(self, id: str) -> None:
        pass

    @abstractmethod
    def update(self, thought: Thought) -> None:
        pass
