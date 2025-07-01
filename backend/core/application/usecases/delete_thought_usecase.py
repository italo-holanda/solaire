from pydantic import BaseModel

from backend.core.domain.repositories.thought_repository import ThoughtRepository
from backend.core.domain.repositories.thought_vector_store import ThoughtVectorStore

class DeleteThoughtDTO(BaseModel):
    thought_id: str

class DeleteThoughtUsecase:

    def __init__(
        self,
        thought_repository: ThoughtRepository,
        thougth_vector_store: ThoughtVectorStore
    ):
        self.thought_repository = thought_repository
        self.thougth_vector_store = thougth_vector_store

    def execute(self, dto: DeleteThoughtDTO) -> None:
        self.thought_repository.delete(dto.thought_id)
        self.thougth_vector_store.delete_index(dto.thought_id)