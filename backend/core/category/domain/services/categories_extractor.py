from abc import ABC, abstractmethod
from typing import List

from backend.core.thought.domain.entities.thought import Thought


class CategoriesExtractor(ABC):

    @abstractmethod
    def extract(thought: Thought) -> List[str]:
        pass
