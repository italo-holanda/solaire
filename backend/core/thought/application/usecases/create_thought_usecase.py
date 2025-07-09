from pydantic import BaseModel, ValidationError

from backend.core.common.domain.exceptions.application_exception import ApplicationException
from backend.core.thought.domain.entities.thought import Thought
from backend.core.thought.domain.repositories.thought_repository import ThoughtRepositoryInterface
from backend.core.thought.domain.repositories.thought_vector_store import ThoughtVectorStoreInterface
from backend.core.thought.domain.services.thought_interpreter import ThoughtInterpreterInterface


class CreateThoughtDTO(BaseModel):
    text: str


class CreateThoughtUsecase ():
    def __init__(
        self,
        thought_interpreter: ThoughtInterpreterInterface,
        thought_repository: ThoughtRepositoryInterface,
        thought_vector_store: ThoughtVectorStoreInterface
    ):
        self.thought_interpreter = thought_interpreter
        self.thought_repository = thought_repository
        self.thought_vector_store = thought_vector_store

    def execute(self, dto: CreateThoughtDTO):

        try:
            thought = Thought(
                text=dto.text,
                summary='',
                title='',
                categories=[],
                embeddings=[]
            )
        except ValidationError:
            raise ApplicationException('Invalid thought object', 400)

        interpreter_output = self.thought_interpreter.invoke(thought)

        thought.summary = interpreter_output.summary
        thought.title = interpreter_output.title
        thought.categories = interpreter_output.categories

        self.thought_repository.save(thought)
        self.thought_vector_store.create_index(thought)
