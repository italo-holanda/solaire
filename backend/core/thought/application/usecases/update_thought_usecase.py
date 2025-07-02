from pydantic import BaseModel

from backend.core.thought.domain.repositories.thought_repository import ThoughtRepository
from backend.core.thought.domain.repositories.thought_vector_store import ThoughtVectorStore
from backend.core.category.domain.services.categories_extractor import CategoriesExtractor
from backend.core.thought.domain.services.thought_summary_generator import SummaryGenerator
from backend.core.thought.domain.services.thought_title_generator import TitleGenerator


class UpdateThoughtDTO(BaseModel):
    thought_id: str
    text: str


class UpdateThoughtUsecase ():
    def __init__(
        self,
        summary_generator: SummaryGenerator,
        title_generator: TitleGenerator,
        categories_extractor: CategoriesExtractor,
        thought_repository: ThoughtRepository,
        thought_vector_store: ThoughtVectorStore
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
        if len(dto.text) < 100 or len(dto.text > 1000):
            raise ValueError('Text must be > 100 and <= 1000')

        thought.summary = self.summary_generator.generate(thought)
        thought.title = self.title_generator.generate(thought)
        thought.categories = self.categories_extractor.extract(thought)

        self.thought_repository.update(thought.id, thought.text)
        self.thought_vector_store.delete_index(thought)
        self.thought_vector_store.create_index(thought)
