
from abc import ABC, abstractmethod
from typing import List

from pydantic import BaseModel

from src.core.thought.domain.entities.thought import Thought


class ThoughtTopicSuggesterOutput(BaseModel):
    suggested_topics: List[str]


class ThoughtTopicSuggesterInterface(ABC):

    @abstractmethod
    def invoke(
        self,
        main_thought: Thought,
        similar_thoughts: List[Thought]
    ) -> ThoughtTopicSuggesterOutput:
        pass
