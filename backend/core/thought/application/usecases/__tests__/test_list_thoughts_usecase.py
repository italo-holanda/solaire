import pytest

from unittest.mock import Mock
from faker import Faker

from backend.core.thought.application.usecases.list_thoughts_usecase import ListThoughtsDTO, ListThoughtsUsecase
from backend.core.thought.domain.entities.thought import Thought

faker = Faker()


class TestListThoughtsUsecase:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.dependencies = {
            "thought_repository": Mock(),
            "thought_vector_store": Mock()
        }

        self.usecase = ListThoughtsUsecase(
            thought_repository=self.dependencies.get('thought_repository'),
            thought_vector_store=self.dependencies.get('thought_vector_store')
        )

        """
        1. Should return all thoughts when search_term is None
        2. Should return all thoughts when search_term is empty
        3. Should return filtered thoughts when search_term is provided
        """

    def test__should_return_all_thoughts_when_search_term_is_none(self):
        thoughts = [
            Mock(spec=Thought),
            Mock(spec=Thought),
            Mock(spec=Thought)
        ]
        self.dependencies["thought_repository"].list.return_value = thoughts

        result = self.usecase.execute(ListThoughtsDTO(search_term=None))

        assert result == thoughts
        self.dependencies["thought_repository"].list.assert_called_once()

    def test__should_return_all_thoughts_when_search_term_is_empty(self):
        thoughts = [
            Mock(spec=Thought),
            Mock(spec=Thought)
        ]
        self.dependencies["thought_repository"].list.return_value = thoughts

        result = self.usecase.execute(ListThoughtsDTO(search_term=""))

        assert result == thoughts
        self.dependencies["thought_repository"].list.assert_called_once()

    def test__should_return_filtered_thoughts_when_search_term_is_provided(self):
        search_term = "python programming"
        filtered_thoughts = [
            Mock(spec=Thought),
            Mock(spec=Thought)
        ]
        
        self.dependencies["thought_vector_store"] \
            .search_similar_by_text.return_value = filtered_thoughts

        result = self.usecase.execute(
            ListThoughtsDTO(search_term=search_term)
        )

        assert result == filtered_thoughts
        
        self.dependencies["thought_vector_store"] \
            .search_similar_by_text.assert_called_once()
        
        call_args = self.dependencies["thought_vector_store"] \
            .search_similar_by_text.call_args

        assert call_args.kwargs['thought_text'] == search_term
