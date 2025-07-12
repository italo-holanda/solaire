import pytest

from unittest.mock import Mock
from faker import Faker

from backend.core.common.domain.exceptions.application_exception import ApplicationException
from backend.core.thought.application.usecases.update_thought_usecase import UpdateThoughtDTO, UpdateThoughtUsecase
from backend.core.thought.domain.entities.thought import Thought
from backend.core.thought.domain.services.thought_interpreter import ThoughtInterpreterOutput

faker = Faker()


class TestUpdateThoughtUsecase:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.dependencies = {
            "thought_interpreter": Mock(),
            "thought_repository": Mock(),
            "thought_vector_store": Mock(),
            "category_repository": Mock()
        }

        self.usecase = UpdateThoughtUsecase(
            thought_interpreter=self.dependencies.get('thought_interpreter'),
            thought_repository=self.dependencies.get('thought_repository'),
            thought_vector_store=self.dependencies.get('thought_vector_store'),
            category_repository=self.dependencies.get('category_repository'),
        )

        """
        1. Should throw error when thought is not found
        2. Should throw error when text is empty
        3. Should throw error when text is too short
        4. Should throw error when text is too long
        5. Should update thought when text is valid
        6. Should regenerate summary, title and categories
        7. Should update repository and vector store
        """

    def test__should_throw_error_when_thought_is_not_found(self):
        thought_id = faker.uuid4()
        self.dependencies["thought_repository"].get_by_id.return_value = None

        with pytest.raises(ApplicationException, match="Thought not found"):
            self.usecase.execute(
                UpdateThoughtDTO(
                    thought_id=thought_id,
                    text="Valid text " * 20
                )
            )

        self.dependencies["thought_repository"].get_by_id \
            .assert_called_once_with(thought_id)

    def test__should_throw_error_when_text_is_empty(self):
        thought_id = faker.uuid4()

        with pytest.raises(ApplicationException, match="Thought text is required"):
            self.usecase.execute(
                UpdateThoughtDTO(
                    thought_id=thought_id,
                    text=""
                )
            )

    def test__should_throw_error_when_text_is_too_short(self):
        thought_id = faker.uuid4()
        short_text = "Short text"

        thought = Thought(
            id=thought_id,
            text=faker.text(max_nb_chars=300),
            categories=[],
            summary="Example of summary",
            title="Example of title",
            embeddings=[]
        )

        self.dependencies["thought_repository"].get_by_id.return_value = thought

        self.dependencies["thought_interpreter"].invoke.return_value = ThoughtInterpreterOutput(
            categories=[],
            summary="Example of summary ......",
            title="Example of title ......"
        )

        with pytest.raises(ApplicationException):
            self.usecase.execute(
                UpdateThoughtDTO(
                    thought_id=thought_id,
                    text=short_text
                )
            )

    def test__should_throw_error_when_text_is_too_long(self):
        thought_id = faker.uuid4()
        long_text = "Very long text " * 100  # More than 1000 characters

        thought = Thought(
            id=thought_id,
            text=faker.text(max_nb_chars=300),
            categories=[],
            summary="Example of summary",
            title="Example of title",
            embeddings=[]
        )

        self.dependencies["thought_repository"].get_by_id.return_value = thought
        self.dependencies["thought_interpreter"].invoke.return_value = ThoughtInterpreterOutput(
            categories=[],
            summary="Example of summary ......",
            title="Example of title ......"
        )

        with pytest.raises(ApplicationException):
            self.usecase.execute(
                UpdateThoughtDTO(
                    thought_id=thought_id,
                    text=long_text
                )
            )

    def test__should_update_thought_when_text_is_valid(self):
        thought_id = faker.uuid4()
        valid_text = faker.text(max_nb_chars=300)

        thought = Mock(spec=Thought)
        thought.id = thought_id
        thought.text = valid_text

        self.dependencies["thought_repository"].get_by_id.return_value = thought
        self.dependencies["thought_interpreter"].invoke.return_value = ThoughtInterpreterOutput(
            categories=[],
            summary="Example of summary ......",
            title="Example of title ......"
        )
        
        self.usecase.execute(
            UpdateThoughtDTO(thought_id=thought_id, text=valid_text)
        )

        # The update is called twice: once immediately and once in the async thread
        assert self.dependencies["thought_repository"].update.call_count == 2
        self.dependencies["thought_repository"].update \
            .assert_any_call(thought)

        assert thought.text == valid_text

    def test__should_regenerate_summary_title_and_categories(self):
        thought_id = faker.uuid4()
        valid_text = faker.text(max_nb_chars=300)

        thought = Mock(spec=Thought)
        thought.id = thought_id
        thought.text = valid_text

        self.dependencies["thought_repository"].get_by_id.return_value = thought
        self.dependencies["thought_interpreter"].invoke.return_value = ThoughtInterpreterOutput(
            categories=[],
            summary="Example of summary ......",
            title="Example of title ......"
        )

        self.usecase.execute(
            UpdateThoughtDTO(thought_id=thought_id, text=valid_text)
        )

        self.dependencies["thought_interpreter"].invoke \
            .assert_called_once_with(thought)

    def test__should_update_repository_and_vector_store(self):
        thought_id = faker.uuid4()
        valid_text = faker.text(max_nb_chars=300)

        thought = Mock(spec=Thought)
        thought.id = thought_id
        thought.text = valid_text

        self.dependencies["thought_repository"].get_by_id.return_value = thought
        self.dependencies["thought_interpreter"].invoke.return_value = ThoughtInterpreterOutput(
            categories=[],
            summary="Example of summary ......",
            title="Example of title ......"
        )


        self.usecase.execute(
            UpdateThoughtDTO(thought_id=thought_id, text=valid_text)
        )

        # The update is called twice: once immediately and once in the async thread
        assert self.dependencies["thought_repository"].update.call_count == 2
        self.dependencies["thought_repository"].update \
            .assert_any_call(thought)
        self.dependencies["thought_vector_store"].create_index \
            .assert_called_once_with(thought)
