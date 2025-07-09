from unittest.mock import Mock
from faker import Faker
from pydantic import ValidationError
import pytest

from backend.core.thought.application.usecases.create_thought_usecase import CreateThoughtDTO, CreateThoughtUsecase
from backend.core.thought.domain.services.thought_interpreter import ThoughtInterpreterOutput


faker = Faker()


class TestCreateThoughtUsecase:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.dependencies = {
            "thought_interpreter": Mock(),
            "thought_repository": Mock(),
            "thought_vector_store": Mock()
        }

        self.usecase = CreateThoughtUsecase(
            thought_interpreter=self.dependencies.get('thought_interpreter'),
            thought_repository=self.dependencies.get('thought_repository'),
            thought_vector_store=self.dependencies.get('thought_vector_store'),
        )

        """
        1. Should throw error when text is None
        2. Should throw error when text is lower than 100 chars
        3. Should save the thought when text is valid
        4. Should create embeddings when text is valid
        """

    def test__should_throw_error_when_text_is_none(self):
        with pytest.raises(ValidationError):
            self.usecase.execute(CreateThoughtDTO(text=None))

    def test__should_throw_error_when_text_is_lower_than_100_chars(self):
        with pytest.raises(ValueError):
            self.usecase.execute(CreateThoughtDTO(text=""))
        with pytest.raises(ValueError):
            self.usecase.execute(CreateThoughtDTO(text="Lorem Ipsum"))
        with pytest.raises(ValueError):
            self.usecase.execute(CreateThoughtDTO(text=" " * 100 + " Hello"))
        with pytest.raises(ValueError):
            self.usecase.execute(CreateThoughtDTO(
                text=f"Hello {" " * 100}, how are you?"))

    def test__should_throw_error_when_text_is_bigger_than_1000_chars(self):
        def get_1001_chars_text():
            text = ""
            while len(text) < 1001:
                text += " " + faker.text(max_nb_chars=200)
            return text.strip()

        with pytest.raises(ValueError):
            self.usecase.execute(CreateThoughtDTO(text=get_1001_chars_text()))

    def test__should_save_thought_when_text_is_valid(self):
        self.dependencies["thought_interpreter"].invoke.return_value = ThoughtInterpreterOutput(
            categories=[],
            summary="Example of summary ......",
            title="Example of title ......"
        )

        valid_text = faker.text(max_nb_chars=300)

        self.usecase.execute(CreateThoughtDTO(text=valid_text))

        self.dependencies["thought_repository"].save.assert_called_once()
        saved_thought = self.dependencies["thought_repository"].save.call_args[0][0]

        assert saved_thought.text == valid_text

    def test__should_create_embeddings_when_text_is_valid(self):
        self.dependencies["thought_interpreter"].invoke.return_value = ThoughtInterpreterOutput(
            categories=[],
            summary="Example of summary ......",
            title="Example of title ......"
        )

        valid_text = faker.text(max_nb_chars=300)

        self.usecase.execute(CreateThoughtDTO(text=valid_text))

        self.dependencies["thought_vector_store"].create_index.assert_called_once()
        indexed_thought = self.dependencies["thought_vector_store"].create_index.call_args[0][0]

        assert indexed_thought.text == valid_text

    def test__should_call_thought_interpreter(self):
        self.dependencies["thought_interpreter"].invoke.return_value = ThoughtInterpreterOutput(
            categories=[],
            summary="Example of summary ......",
            title="Example of title ......"
        )

        valid_text = faker.text(max_nb_chars=300)

        self.usecase.execute(CreateThoughtDTO(text=valid_text))

        self.dependencies["thought_interpreter"].invoke.assert_called_once()

        self.dependencies["thought_vector_store"].create_index.assert_called_once()
        indexed_thought = self.dependencies["thought_vector_store"].create_index.call_args[0][0]

        assert indexed_thought.text == valid_text
