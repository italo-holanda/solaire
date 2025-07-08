from abc import ABC, abstractmethod
from typing import List

from backend.core.thought.domain.entities.thought import Thought


class ThoughtRepositoryInterface(ABC):

    @abstractmethod
    def save(thought: Thought) -> None:
        pass

    @abstractmethod
    def get_by_id(id: str) -> Thought:
        pass

    @abstractmethod
    def list() -> List[Thought]:
        pass

    @abstractmethod
    def delete(id: str) -> None:
        pass

    @abstractmethod
    def update(thought: Thought) -> None:
        pass
