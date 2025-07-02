from abc import ABC, abstractmethod
from typing import List

from backend.core.thought.domain.entities.thought import Thought


class ThoughtTopicSuggester(ABC):

    @abstractmethod
    def suggest(
        main_thought: Thought,
        similar_thoughts: List[Thought]
    ) -> List[str]:
        pass
