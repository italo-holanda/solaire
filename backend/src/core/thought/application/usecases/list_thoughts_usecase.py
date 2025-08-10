from typing import List, Optional

from pydantic import BaseModel

from src.core.thought.domain.entities.thought import Thought
from src.core.thought.domain.repositories.thought_repository import ThoughtRepositoryInterface
from src.core.thought.domain.repositories.thought_vector_store import ThoughtVectorStoreInterface


class ListThoughtsDTO(BaseModel):
    search_term: Optional[str]
    category_ids: Optional[List[str]]


class ListThoughtsUsecase:
    def __init__(
        self,
        thought_repository: ThoughtRepositoryInterface,
        thought_vector_store: ThoughtVectorStoreInterface
    ):
        self.thought_repository = thought_repository
        self.thought_vector_store = thought_vector_store

    def execute(self, dto: ListThoughtsDTO) -> List[Thought]:
        if not dto.search_term and not dto.category_ids:
            return self.thought_repository.list()
        
        if dto.search_term and not dto.category_ids:
            vector_results = self.thought_vector_store.search_similar_by_text(
                thought_text=f"{dto.search_term}"
            )
            thoughts: List[Thought] = []
            for vector in vector_results:
                thought = self.thought_repository.get_by_id(vector.thought_id)
                if thought:
                    thoughts.append(thought)
            return thoughts
        
        if dto.category_ids and not dto.search_term:
            return self.thought_repository.list_by_categories(dto.category_ids)
        
        if dto.search_term and dto.category_ids:
            vector_results = self.thought_vector_store.search_similar_by_text(
                thought_text=f"{dto.search_term}"
            )
            thoughts: List[Thought] = []
            for vector in vector_results:
                thought = self.thought_repository.get_by_id(vector.thought_id)
                if thought:
                    thoughts.append(thought)
            
            category_filtered_thoughts = self.thought_repository.list_by_categories(dto.category_ids)
            category_filtered_ids = {thought.id for thought in category_filtered_thoughts}
            
            return [thought for thought in thoughts if thought.id in category_filtered_ids]
        
        return []
