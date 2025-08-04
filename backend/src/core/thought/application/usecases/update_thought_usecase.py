import threading
from pydantic import BaseModel

from src.core.common.domain.exceptions.application_exception import ApplicationException
from src.core.thought.domain.repositories.thought_repository import ThoughtRepositoryInterface
from src.core.thought.domain.repositories.thought_vector_store import ThoughtVectorStoreInterface
from src.core.thought.domain.services.thought_interpreter import ThoughtInterpreterInterface
from src.core.category.domain.repositories.category_repository import CategoryRepositoryInterface


class UpdateThoughtDTO(BaseModel):
    thought_id: str
    text: str


class UpdateThoughtUsecase:
    def __init__(
        self,
        thought_interpreter: ThoughtInterpreterInterface,
        thought_repository: ThoughtRepositoryInterface,
        thought_vector_store: ThoughtVectorStoreInterface,
        category_repository: CategoryRepositoryInterface,
    ):
        self.thought_interpreter = thought_interpreter
        self.thought_repository = thought_repository
        self.thought_vector_store = thought_vector_store
        self.category_repository = category_repository

    def execute(self, dto: UpdateThoughtDTO):
        thought = self.thought_repository.get_by_id(dto.thought_id)

        if not thought:
            raise ApplicationException("Thought not found", 404)
        if not dto.text:
            raise ApplicationException("Thought text is required", 400)

        try:
            thought.text = dto.text
        except ValueError:
            raise ApplicationException("Invalid thought text", code=400)

        self.thought_repository.update(thought)
        self.thought_vector_store.create_index(thought)

        def _async_interpret_and_update(thought):
            interpreter_output = self.thought_interpreter.invoke(thought)
            thought.summary = interpreter_output.summary
            thought.title = interpreter_output.title

            thought.categories = []
            for category in interpreter_output.categories:
                category_found = self.category_repository.get_by_name(
                    category.name)
                if category_found:
                    category.id = category_found.id
                else:
                    self.category_repository.save(category)
                thought.categories.append(category)

            self.thought_repository.update(thought)

        threading.Thread(target=_async_interpret_and_update,
                         args=(thought,)).start()
