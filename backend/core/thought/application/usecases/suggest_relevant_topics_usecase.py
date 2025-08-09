from typing import List
from pydantic import BaseModel

from backend.core.common.domain.exceptions.application_exception import ApplicationException
from backend.core.thought.application.usecases.list_related_thoughts_usecase import ListRelatedThoughtsUsecase
from backend.core.thought.domain.repositories.thought_repository import ThoughtRepositoryInterface
from backend.core.thought.domain.services.thought_topic_suggester import ThoughtTopicSuggesterInterface

class SuggestRelevantTopicsDTO(BaseModel):
    thought_id: str


class SuggestRelevantTopicsUsecase:
    def __init__(
        self,
        list_related_thoughts_usecase: ListRelatedThoughtsUsecase,
        topic_suggester: ThoughtTopicSuggesterInterface,
        thought_repository: ThoughtRepositoryInterface
    ):
        self.list_related_thoughts_usecase = list_related_thoughts_usecase
        self.topic_suggester = topic_suggester
        self.thought_repository = thought_repository

    def execute(self, dto: SuggestRelevantTopicsDTO) -> List[str]:
        main_thought = self.thought_repository.get_by_id(dto.thought_id)

        if not main_thought:
            raise ApplicationException("Thought not found", 404)

        similar_thoughts = self.list_related_thoughts_usecase \
            .execute(dto)

        new_suggestions = self.topic_suggester.invoke(
            main_thought,
            similar_thoughts
        )

        return new_suggestions.suggested_topics
