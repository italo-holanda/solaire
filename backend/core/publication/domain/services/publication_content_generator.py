from abc import ABC, abstractmethod
from typing import List, Optional

from backend.core.thought.domain.entities.thought import Thought


class PublicationContentGenerator(ABC):

    @abstractmethod
    def generate(
        thoughts: List[Thought],
        user_guideline: Optional[str],
        outlining: List[str]

    ) -> str:
        pass
