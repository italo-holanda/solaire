

# -- DEPS -------------

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from pydantic import BaseModel, Field
from typing import List, Optional


class Entity(BaseModel):
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    deleted_at: Optional[datetime] = None


class Thought(Entity):
    id: str
    title: str
    summary: str
    text: str
    categories: List[str]
    embeddings: List[float]


class SummaryGenerator(ABC):

    @abstractmethod
    def generate(thought: Thought) -> str:
        pass


class TitleGenerator(ABC):

    @abstractmethod
    def generate(thought: Thought) -> str:
        pass


class CategoriesExtractor(ABC):

    @abstractmethod
    def extract(thought: Thought) -> List[str]:
        pass


class ThoughtRepository(ABC):

    @abstractmethod
    def save(thought: Thought) -> None:
        pass

    @abstractmethod
    def get_by_id(id: str) -> Thought:
        pass

    @abstractmethod
    def list() -> List[Thought]:
        pass


class ThoughtVectorStore(ABC):
    @abstractmethod
    def create_index(thought: Thought) -> None:
        pass


# ---------------------

class CreateThoughtDTO(BaseModel):
    text: str


class CreateThoughtUsecase ():
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

    def execute(self, dto: CreateThoughtDTO):

        if not dto.text:
            raise ValueError("Thought text is required")
        if len(dto.text) < 100 or len(dto.text > 1000):
            raise ValueError('Text must be > 100 and <= 1000')

        thought = Thought(
            text=dto.text,
            summary='',
            categories=[],
            embeddings=[]
        )

        thought.summary = self.summary_generator.generate(thought)
        thought.title = self.title_generator.generate(thought)
        thought.categories = self.categories_extractor.extract(thought)

        self.thought_repository.save(thought)
        self.thought_vector_store.create_index(thought)
