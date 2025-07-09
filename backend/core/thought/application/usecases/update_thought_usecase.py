from pydantic import BaseModel

from backend.core.common.domain.exceptions.application_exception import ApplicationException
from backend.core.thought.domain.repositories.thought_repository import ThoughtRepositoryInterface
from backend.core.thought.domain.repositories.thought_vector_store import ThoughtVectorStoreInterface
from backend.core.category.domain.services.categories_extractor import CategoriesExtractor
from backend.core.thought.domain.services.thought_summary_generator import ThoughtSummaryGenerator
from backend.core.thought.domain.services.thought_title_generator import ThoughtTitleGenerator


class UpdateThoughtDTO(BaseModel):
    thought_id: str
    text: str


class UpdateThoughtUsecase ():
    def __init__(
        self,
        summary_generator: ThoughtSummaryGenerator,
        title_generator: ThoughtTitleGenerator,
        categories_extractor: CategoriesExtractor,
        thought_repository: ThoughtRepositoryInterface,
        thought_vector_store: ThoughtVectorStoreInterface
    ):
        self.summary_generator = summary_generator
        self.title_generator = title_generator
        self.categories_extractor = categories_extractor
        self.thought_repository = thought_repository
        self.thought_vector_store = thought_vector_store

    def execute(self, dto: UpdateThoughtDTO):
        thought = self.thought_repository.get_by_id(dto.thought_id)

        if not thought:
            raise ApplicationException("Thought not found", 404)
        if not dto.text:
            raise ApplicationException("Thought text is required", 400)

        try:
            thought.summary = self.summary_generator.generate(thought)
            thought.title = self.title_generator.generate(thought)
            thought.categories = self.categories_extractor.extract(thought)
            thought.text = dto.text
        except ValueError:
            raise ApplicationException('Invalid thought', 400)

        self.thought_repository.update(thought)
        self.thought_vector_store.delete_index(thought)
        self.thought_vector_store.create_index(thought)
