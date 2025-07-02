from abc import ABC, abstractmethod

from backend.core.thought.domain.entities.thought import Thought


class ThoughtTitleGenerator(ABC):

    @abstractmethod
    def generate(thought: Thought) -> str:
        pass
