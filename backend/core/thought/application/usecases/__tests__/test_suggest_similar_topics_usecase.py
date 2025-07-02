import pytest

from unittest.mock import Mock
from faker import Faker

from backend.core.thought.application.usecases.suggest_similar_topics_usecase import SuggestSimilarTopicsDTO, SuggestSimilarTopicsUsecase
from backend.core.thought.domain.entities.thought import Thought

faker = Faker()


class TestSuggestSimilarTopicsUsecase:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.dependencies = {
            "list_related_thoughts_usecase": Mock(),
            "topic_suggester": Mock(),
            "thought_repository": Mock()
        }

        self.usecase = SuggestSimilarTopicsUsecase(
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

        with pytest.raises(ValueError, match="Thought not found"):
            self.usecase.execute(
                SuggestSimilarTopicsDTO(thought_id=thought_id))

        self.dependencies["thought_repository"].get_by_id \
            .assert_called_once_with(thought_id)

    def test__should_return_topic_suggestions_when_thought_is_found(self):
        thought_id = faker.uuid4()
        main_thought = Mock(spec=Thought)
        main_thought.id = thought_id

        similar_thoughts = [
            Mock(spec=Thought),
            Mock(spec=Thought)
        ]

        expected_suggestions = ["Python", "Programming", "AI"]

        self.dependencies["thought_repository"].get_by_id.return_value = main_thought
        self.dependencies["list_related_thoughts_usecase"].execute.return_value = similar_thoughts
        self.dependencies["topic_suggester"].suggest.return_value = expected_suggestions

        result = self.usecase.execute(
            SuggestSimilarTopicsDTO(thought_id=thought_id)
        )

        assert result == expected_suggestions

    def test__should_call_topic_suggester(self):
        thought_id = faker.uuid4()
        main_thought = Mock(spec=Thought)
        main_thought.id = thought_id

        similar_thoughts = [
            Mock(spec=Thought),
            Mock(spec=Thought)
        ]

        suggestions = ["Topic 1"]

        self.dependencies["thought_repository"].get_by_id.return_value = main_thought
        self.dependencies["list_related_thoughts_usecase"].execute.return_value = similar_thoughts
        self.dependencies["topic_suggester"].suggest.return_value = suggestions

        self.usecase.execute(
            SuggestSimilarTopicsDTO(thought_id=thought_id)
        )

        self.dependencies["topic_suggester"].suggest \
            .assert_called_once_with(main_thought, similar_thoughts)
