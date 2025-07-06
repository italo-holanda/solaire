from typing import List, Optional

from pydantic import BaseModel

from backend.core.thought.domain.entities.thought import Thought
from backend.core.thought.domain.repositories.thought_repository import ThoughtRepositoryInterface
from backend.core.thought.domain.repositories.thought_vector_store import ThoughtVectorStoreInterface


class ListThoughtsDTO(BaseModel):
    search_term: Optional[str]


class ListThoughtsUsecase:
    def __init__(
        self,
        thought_repository: ThoughtRepositoryInterface,
        thought_vector_store: ThoughtVectorStoreInterface
    ):
        self.thought_repository = thought_repository
        self.thought_vector_store = thought_vector_store

    def execute(self, dto: ListThoughtsDTO) -> List[Thought]:
        if not dto.search_term:
            return self.thought_repository.list()
        return self.thought_vector_store.search_similar_by_text(
            thought_text=f'{dto.search_term}'
        )
