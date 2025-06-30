from abc import ABC, abstractmethod

from backend.core.domain.entities.thought import Thought


class SummaryGenerator(ABC):

    @abstractmethod
    def generate(thought: Thought) -> str:
        pass
