from typing import List, Optional

from pydantic import BaseModel

from backend.core.domain.entities.thought import Thought
from backend.core.domain.repositories.thought_repository import ThoughtRepository
from backend.core.domain.repositories.thought_vector_store import ThoughtVectorStore


class ListThoughtsDTO(BaseModel):
    search_term: Optional[str]


class ListThoughtsUsecase:
    def __init__(
        self,
        thought_repository: ThoughtRepository,
        thought_vector_store: ThoughtVectorStore
    ):
        self.thought_repository = thought_repository
        self.thought_vector_store = thought_vector_store

    def execute(self, dto: ListThoughtsDTO) -> List[Thought]:
        if not dto.search_term:
            return self.thought_repository.list()
        return self.thought_vector_store.search_similar(
            Thought(text=f'{dto.search_term}')
        )
