import pytest

from unittest.mock import Mock
from faker import Faker

from backend.core.thought.application.usecases.delete_thought_usecase import DeleteThoughtDTO, DeleteThoughtUsecase

faker = Faker()


class TestDeleteThoughtUsecase:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.dependencies = {
            "thought_repository": Mock(),
            "thought_vector_store": Mock()
        }

        self.usecase = DeleteThoughtUsecase(
            thought_repository=self.dependencies.get('thought_repository'),
            thought_vector_store=self.dependencies.get('thought_vector_store')
        )

        """
        1. Should delete the thought
        2. Should delete the embeddings
        """

    def test__should_delete_thought(self):
        thought_id = faker.uuid4()

        self.usecase.execute(DeleteThoughtDTO(thought_id=thought_id))

        self.dependencies["thought_repository"].delete.assert_called_once()
        deleted_thought = self.dependencies["thought_repository"].delete.call_args[0][0]

        assert deleted_thought == thought_id

    def test__should_delete_thought_index(self):
        thought_id = faker.uuid4()

        self.usecase.execute(DeleteThoughtDTO(thought_id=thought_id))

        self.dependencies["thought_vector_store"].delete_index.assert_called_once()
        deleted_thought = self.dependencies["thought_vector_store"].delete_index.call_args[0][0]

        assert deleted_thought == thought_id

