from pydantic import BaseModel

from backend.core.common.domain.util import remove_extra_spaces
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
            raise ValueError("Thought not found")
        if not dto.text:
            raise ValueError("Thought text is required")
        if len(remove_extra_spaces(dto.text)) <= 100 or len(remove_extra_spaces(dto.text)) > 1000:
            raise ValueError('Text must be >= 100 and <= 1000')

        thought.summary = self.summary_generator.generate(thought)
        thought.title = self.title_generator.generate(thought)
        thought.categories = self.categories_extractor.extract(thought)

        self.thought_repository.update(thought.id, thought.text)
        self.thought_vector_store.delete_index(thought)
        self.thought_vector_store.create_index(thought)
