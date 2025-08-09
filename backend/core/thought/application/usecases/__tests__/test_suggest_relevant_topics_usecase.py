import pytest

from unittest.mock import Mock
from faker import Faker

from backend.core.common.domain.exceptions.application_exception import ApplicationException
from backend.core.thought.application.usecases.suggest_relevant_topics_usecase import SuggestRelevantTopicsDTO, SuggestRelevantTopicsUsecase
from backend.core.thought.domain.entities.thought import Thought
from backend.core.thought.domain.services.thought_topic_suggester import ThoughtTopicSuggesterOutput

faker = Faker()


class TestSuggestRelevantTopicsUsecase:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.dependencies = {
            "list_related_thoughts_usecase": Mock(),
            "topic_suggester": Mock(),
            "thought_repository": Mock()
        }

        self.usecase = SuggestRelevantTopicsUsecase(
            list_related_thoughts_usecase=self.dependencies.get(
                'list_related_thoughts_usecase'),
            topic_suggester=self.dependencies.get('topic_suggester'),
            thought_repository=self.dependencies.get('thought_repository')
        )

        """
        1. Should throw error when thought is not found
        2. Should return topic suggestions when thought is found
        3. Should call topic_suggester
        """

    def test__should_throw_error_when_thought_is_not_found(self):
        thought_id = faker.uuid4()
        self.dependencies["thought_repository"].get_by_id.return_value = None

        with pytest.raises(ApplicationException, match="Thought not found"):
            self.usecase.execute(
                SuggestRelevantTopicsDTO(thought_id=thought_id))

        self.dependencies["thought_repository"].get_by_id \
            .assert_called_once_with(thought_id)

    def test__should_return_topic_suggestions_when_thought_is_found(self):
        thought_id = faker.uuid4()
        main_thought = Mock(spec=Thought)
        main_thought.id = thought_id

        relevant_thoughts = [
            Mock(spec=Thought),
            Mock(spec=Thought)
        ]

        expected_suggestions = ["Python", "Programming", "AI"]

        self.dependencies["thought_repository"].get_by_id.return_value = main_thought
        self.dependencies["list_related_thoughts_usecase"].execute.return_value = relevant_thoughts
        self.dependencies["topic_suggester"].invoke.return_value = ThoughtTopicSuggesterOutput(suggested_topics=expected_suggestions)

        result = self.usecase.execute(
            SuggestRelevantTopicsDTO(thought_id=thought_id)
        )

        assert result == expected_suggestions

    def test__should_call_topic_suggester(self):
        thought_id = faker.uuid4()
        main_thought = Mock(spec=Thought)
        main_thought.id = thought_id

        relevant_thoughts = [
            Mock(spec=Thought),
            Mock(spec=Thought)
        ]

        suggestions = ["Topic 1"]

        self.dependencies["thought_repository"].get_by_id.return_value = main_thought
        self.dependencies["list_related_thoughts_usecase"].execute.return_value = relevant_thoughts
        self.dependencies["topic_suggester"].invoke.return_value = ThoughtTopicSuggesterOutput(suggested_topics=suggestions)

        self.usecase.execute(
            SuggestRelevantTopicsDTO(thought_id=thought_id)
        )

        self.dependencies["topic_suggester"].invoke \
            .assert_called_once_with(main_thought, relevant_thoughts)
