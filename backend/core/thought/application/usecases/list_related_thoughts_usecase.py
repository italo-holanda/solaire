from typing import List
from pydantic import BaseModel

from backend.core.common.domain.exceptions.application_exception import (
    ApplicationException,
)
from backend.core.thought.domain.entities.thought import Thought
from backend.core.thought.domain.repositories.thought_repository import (
    ThoughtRepositoryInterface,
)
from backend.core.thought.domain.repositories.thought_vector_store import (
    ThoughtVectorStoreInterface,
)


class ListRelatedThoughtsDTO(BaseModel):
    thought_id: str


class ListRelatedThoughtsUsecase:
    def __init__(
        self,
        thought_vector_store: ThoughtVectorStoreInterface,
        thought_repository: ThoughtRepositoryInterface,
    ):
        self.thought_vector_store = thought_vector_store
        self.thought_repository = thought_repository

    def execute(self, dto: ListRelatedThoughtsDTO) -> List[Thought]:
        thought = self.thought_repository.get_by_id(dto.thought_id)

        if not thought:
            raise ApplicationException("Thought not found", 404)

        related_thoughts = []
        for vector in self.thought_vector_store.search_similar(thought):
            if vector.thought_id == dto.thought_id:
                continue
            related = self.thought_repository.get_by_id(vector.thought_id)
            if related:
                related_thoughts.append(related)

        return related_thoughts
