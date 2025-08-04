from abc import ABC, abstractmethod
from typing import List, Optional

from src.core.thought.domain.entities.thought import Thought


class PublicationOutliningGeneratorInterface(ABC):

    @abstractmethod
    def invoke(
        self,
        thoughts: List[Thought],
        user_guideline: Optional[str],

    ) -> List[str]:
        pass
