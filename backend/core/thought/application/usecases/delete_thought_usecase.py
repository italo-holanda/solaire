from pydantic import BaseModel

from backend.core.thought.domain.repositories.thought_repository import ThoughtRepositoryInterface
from backend.core.thought.domain.repositories.thought_vector_store import ThoughtVectorStoreInterface

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
        self.thought_repository.delete(dto.thought_id)
        self.thought_vector_store.delete_index(dto.thought_id)