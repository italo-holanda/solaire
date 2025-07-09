from pydantic import BaseModel

from backend.core.common.domain.exceptions.application_exception import ApplicationException
from backend.core.thought.domain.repositories.thought_repository import ThoughtRepositoryInterface
from backend.core.thought.domain.repositories.thought_vector_store import ThoughtVectorStoreInterface
from backend.core.thought.domain.services.thought_interpreter import ThoughtInterpreterInterface


class UpdateThoughtDTO(BaseModel):
    thought_id: str
    text: str


class UpdateThoughtUsecase ():
    def __init__(
        self,
        thought_interpreter: ThoughtInterpreterInterface,
        thought_repository: ThoughtRepositoryInterface,
        thought_vector_store: ThoughtVectorStoreInterface
    ):
        self.thought_interpreter = thought_interpreter
        self.thought_repository = thought_repository
        self.thought_vector_store = thought_vector_store

    def execute(self, dto: UpdateThoughtDTO):
        thought = self.thought_repository.get_by_id(dto.thought_id)

        if not thought:
            raise ApplicationException("Thought not found", 404)
        if not dto.text:
            raise ApplicationException("Thought text is required", 400)

        interpreter_output = self.thought_interpreter.invoke(thought)

        try:
            thought.text = dto.text
            thought.summary = interpreter_output.summary
            thought.title = interpreter_output.title
            thought.categories = interpreter_output.categories
        except ValueError:
            raise ApplicationException('Invalid thought', 400)

        self.thought_repository.update(thought)
        self.thought_vector_store.delete_index(thought)
        self.thought_vector_store.create_index(thought)
