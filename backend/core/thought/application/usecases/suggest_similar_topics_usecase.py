from typing import List
from pydantic import BaseModel

from backend.core.thought.application.usecases.list_related_thoughts_usecase import ListRelatedThoughtsUsecase
from backend.core.thought.domain.repositories.thought_repository import ThoughtRepositoryInterface
from backend.core.thought.domain.services.thought_topic_suggester import ThoughtTopicSuggester


class SuggestSimilarTopicsDTO(BaseModel):
    thought_id: str


class SuggestSimilarTopicsUsecase:
    def __init__(
        self,
        list_related_thoughts_usecase: ListRelatedThoughtsUsecase,
        topic_suggester: ThoughtTopicSuggester,
        thought_repository: ThoughtRepositoryInterface
    ):
        self.list_related_thoughts_usecase = list_related_thoughts_usecase
        self.topic_suggester = topic_suggester
        self.thought_repository = thought_repository

    def execute(self, dto: SuggestSimilarTopicsDTO) -> List[str]:
        main_thought = self.thought_repository.get_by_id(dto.thought_id)

        if not main_thought:
            raise ValueError("Thought not found")

        similar_thoughts = self.list_related_thoughts_usecase \
            .execute(dto)

        new_suggestions = self.topic_suggester.suggest(
            main_thought,
            similar_thoughts
        )

        return new_suggestions
