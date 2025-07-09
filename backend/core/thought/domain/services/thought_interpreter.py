from abc import ABC, abstractmethod
from typing import List

from pydantic import BaseModel

from backend.core.category.domain.entities.category import Category
from backend.core.thought.domain.entities.thought import Thought


class ThoughtInterpreterOutput(BaseModel):
    title: str
    summary: str
    categories: List[Category]


class ThoughtInterpreterInterface(ABC):

    @abstractmethod
    def invoke(self, thought: Thought) -> ThoughtInterpreterOutput:
        pass
