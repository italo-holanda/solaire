from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import List, Optional

from backend.core.thought.domain.entities.thought import Thought


class PublicationContentOutput(BaseModel):
    title: str
    content: str


class PublicationContentGeneratorInterface(ABC):

    @abstractmethod
    def invoke(
        thoughts: List[Thought],
        user_guideline: Optional[str],
        outlining: List[str]

    ) -> PublicationContentOutput:
        pass
