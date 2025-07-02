from abc import ABC, abstractmethod
from typing import List, Optional

from backend.core.thought.domain.entities.thought import Thought


class PublicationOutliningGenerator(ABC):

    @abstractmethod
    def generate(
        thoughts: list[Thought],
        user_guideline: Optional[str],

    ) -> List[str]:
        pass
