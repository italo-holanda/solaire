from abc import ABC, abstractmethod
from typing import List

from backend.core.domain.entities.thought import Thought


class TopicSuggester(ABC):

    @abstractmethod
    def suggest(
        main_thought: Thought,
        similar_thoughts: List[Thought]
    ) -> List[str]:
        pass
