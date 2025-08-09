from unittest.mock import Mock
from faker import Faker
from pydantic import ValidationError
import pytest

from backend.core.common.domain.exceptions.application_exception import ApplicationException
from backend.core.thought.application.usecases.create_thought_usecase import CreateThoughtDTO, CreateThoughtUsecase
from backend.core.thought.domain.services.thought_interpreter import ThoughtInterpreterOutput


faker = Faker()


class TestCreateThoughtUsecase:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.dependencies = {
            "thought_interpreter": Mock(),
            "thought_repository": Mock(),
            "thought_vector_store": Mock(),
            "category_repository": Mock(),
        }

        self.usecase = CreateThoughtUsecase(
            thought_interpreter=self.dependencies.get('thought_interpreter'),
            thought_repository=self.dependencies.get('thought_repository'),
            thought_vector_store=self.dependencies.get('thought_vector_store'),
            category_repository=self.dependencies.get('category_repository'),
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
        with pytest.raises(ApplicationException):
            self.usecase.execute(CreateThoughtDTO(text=""))
        with pytest.raises(ApplicationException):
            self.usecase.execute(CreateThoughtDTO(text="Lorem Ipsum"))
        with pytest.raises(ApplicationException):
            self.usecase.execute(CreateThoughtDTO(text=" " * 100 + " Hello"))
        with pytest.raises(ApplicationException):
            self.usecase.execute(CreateThoughtDTO(
                text=f"Hello {" " * 100}, how are you?"))

    def test__should_throw_error_when_text_is_bigger_than_1000_chars(self):
        def get_1001_chars_text():
            text = ""
            while len(text) < 1001:
                text += " " + faker.text(max_nb_chars=200)
            return text.strip()

        with pytest.raises(ApplicationException):
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

    def test__should_create_new_category_when_not_found(self):
        from backend.core.category.domain.entities.category import Category
        # Setup interpreter to return a category
        category_name = "NewCategory"
        category = Category(name=category_name)
        self.dependencies["thought_interpreter"].invoke.return_value = ThoughtInterpreterOutput(
            categories=[category],
            summary="summary",
            title="title"
        )
        self.dependencies["category_repository"].get_by_name.return_value = None
        valid_text = faker.text(max_nb_chars=300)
        self.usecase.execute(CreateThoughtDTO(text=valid_text))
        self.dependencies["category_repository"].save.assert_called_once_with(category)
        self.dependencies["thought_repository"].update.assert_called()

    def test__should_use_the_saved_category_id_when_found(self):
        from backend.core.category.domain.entities.category import Category
        # Setup interpreter to return a category
        category_name = "ExistingCategory"
        category = Category(name=category_name)
        found_category = Category(id="existing-id", name=category_name)
        self.dependencies["thought_interpreter"].invoke.return_value = ThoughtInterpreterOutput(
            categories=[category],
            summary="summary",
            title="title"
        )
        self.dependencies["category_repository"].get_by_name.return_value = found_category
        valid_text = faker.text(max_nb_chars=300)
        self.usecase.execute(CreateThoughtDTO(text=valid_text))
        # Should not create a new category
        self.dependencies["category_repository"].save.assert_not_called()
        self.dependencies["thought_repository"].update.assert_called()
        # The category id should be set to the found one
        updated_thought = self.dependencies["thought_repository"].update.call_args[0][0]
        assert updated_thought.categories[0].id == found_category.id

    def test__should_update_thought_repository_with_interpreter_results(self):
        from backend.core.category.domain.entities.category import Category
        # Setup interpreter to return a category and new summary/title
        category_name = "Cat"
        category = Category(name=category_name)
        new_summary = "new summary"
        new_title = "new title"
        self.dependencies["thought_interpreter"].invoke.return_value = ThoughtInterpreterOutput(
            categories=[category],
            summary=new_summary,
            title=new_title
        )
        self.dependencies["category_repository"].get_by_name.return_value = None
        valid_text = faker.text(max_nb_chars=300)
        self.usecase.execute(CreateThoughtDTO(text=valid_text))
        self.dependencies["thought_repository"].update.assert_called()
        updated_thought = self.dependencies["thought_repository"].update.call_args[0][0]
        assert updated_thought.summary == new_summary
        assert updated_thought.title == new_title
        assert updated_thought.categories[0].name == category_name
