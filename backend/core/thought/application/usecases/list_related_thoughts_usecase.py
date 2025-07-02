from typing import List
from pydantic import BaseModel

from backend.core.thought.domain.entities.thought import Thought
from backend.core.thought.domain.repositories.thought_repository import ThoughtRepository
from backend.core.thought.domain.repositories.thought_vector_store import ThoughtVectorStore


class ListRelatedThoughtsDTO(BaseModel):
    thought_id: str


class ListRelatedThoughtsUsecase:
    def __init__(
        self,
        thought_vector_store: ThoughtVectorStore,
        thought_repository: ThoughtRepository,
    ):
        self.thought_vector_store = thought_vector_store
        self.thought_repository = thought_repository

    def execute(self, dto: ListRelatedThoughtsDTO) -> List[Thought]:
        thought = self.thought_repository.get_by_id(dto.thought_id)

        if not thought:
            raise ValueError("Thought not found")

        related_thoughts = []
        for vector in self.thought_vector_store.search_similar(thought):
            related = self.thought_repository.get_by_id(vector.thought_id)
            if related:
                related_thoughts.append(related)

        return related_thoughts
