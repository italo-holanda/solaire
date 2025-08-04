import pytest

from unittest.mock import Mock
from faker import Faker

from src.core.common.domain.exceptions.application_exception import ApplicationException
from src.core.thought.application.usecases.list_related_thoughts_usecase import ListRelatedThoughtsDTO, ListRelatedThoughtsUsecase
from src.core.thought.domain.entities.thought import Thought

faker = Faker()


class TestListRelatedThoughtsUsecase:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.dependencies = {
            "thought_repository": Mock(),
            "thought_vector_store": Mock()
        }

        self.usecase = ListRelatedThoughtsUsecase(
            thought_repository=self.dependencies.get('thought_repository'),
            thought_vector_store=self.dependencies.get('thought_vector_store')
        )

        """
        1. Should throw error when thought is not found
        2. Should return empty list when no related thoughts found
        3. Should return related thoughts when found
        """

    def test__should_throw_error_when_thought_is_not_found(self):
        thought_id = faker.uuid4()
        self.dependencies["thought_repository"].get_by_id.return_value = None

        with pytest.raises(ApplicationException, match="Thought not found"):
            self.usecase.execute(ListRelatedThoughtsDTO(thought_id=thought_id))

    def test__should_return_empty_list_when_no_related_thoughts_found(self):
        thought_id = faker.uuid4()
        thought = Mock(spec=Thought)
        thought.id = thought_id

        self.dependencies["thought_repository"].get_by_id.return_value = thought
        self.dependencies["thought_vector_store"].search_similar.return_value = []

        result = self.usecase.execute(
            ListRelatedThoughtsDTO(thought_id=thought_id)
        )

        assert result == []

        self.dependencies["thought_repository"].get_by_id \
            .assert_called_once_with(thought_id)

        self.dependencies["thought_vector_store"].search_similar \
            .assert_called_once_with(thought)

    def test__should_return_related_thoughts_when_found(self):
        thought_id = faker.uuid4()
        thought = Mock(spec=Thought)
        thought.id = thought_id

        related_thought_1 = Mock(spec=Thought)
        related_thought_1.id = faker.uuid4()

        related_thought_2 = Mock(spec=Thought)
        related_thought_2.id = faker.uuid4()

        vector_1 = Mock()
        vector_1.thought_id = related_thought_1.id

        vector_2 = Mock()
        vector_2.thought_id = related_thought_2.id

        self.dependencies["thought_repository"] \
            .get_by_id.side_effect = [
                thought,
                related_thought_1,
                related_thought_2
        ]

        self.dependencies["thought_vector_store"] \
            .search_similar \
            .return_value = [
                vector_1,
                vector_2
        ]

        result = self.usecase.execute(
            ListRelatedThoughtsDTO(thought_id=thought_id))

        assert len(result) == 2
        assert result[0] == related_thought_1
        assert result[1] == related_thought_2
        assert self.dependencies["thought_repository"].get_by_id.call_count == 3

        self.dependencies["thought_repository"] \
            .get_by_id.assert_any_call(thought_id)

        self.dependencies["thought_repository"] \
            .get_by_id.assert_any_call(related_thought_1.id)

        self.dependencies["thought_repository"] \
            .get_by_id.assert_any_call(related_thought_2.id)

        self.dependencies["thought_vector_store"]. \
            search_similar.assert_called_once_with(thought)
