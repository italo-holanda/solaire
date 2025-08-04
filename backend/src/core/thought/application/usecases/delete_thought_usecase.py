from pydantic import BaseModel

from src.core.thought.domain.repositories.thought_repository import ThoughtRepositoryInterface
from src.core.thought.domain.repositories.thought_vector_store import ThoughtVectorStoreInterface

class DeleteThoughtDTO(BaseModel):
    thought_id: str

class DeleteThoughtUsecase:

    def __init__(
        self,
        thought_repository: ThoughtRepositoryInterface,
        thought_vector_store: ThoughtVectorStoreInterface
    ):
        self.thought_repository = thought_repository
        self.thought_vector_store = thought_vector_store

    def execute(self, dto: DeleteThoughtDTO) -> None:
        # Fetch the Thought object before deletion
        thought = self.thought_repository.get_by_id(dto.thought_id)
        self.thought_repository.delete(dto.thought_id)
        self.thought_vector_store.delete_index(thought)