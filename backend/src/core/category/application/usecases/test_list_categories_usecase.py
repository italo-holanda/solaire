import pytest
from unittest.mock import Mock
from faker import Faker

from core.category.application.usecases.list_categories_usecase import ListCategoriesUsecase
from core.category.domain.entities.category import Category

faker = Faker()

class TestListCategoriesUsecase:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.category_repository = Mock()
        self.usecase = ListCategoriesUsecase(self.category_repository)

    def test__should_return_list_of_categories(self):
        categories = [
            Category(id=faker.uuid4(), name="Tech", color="#ff0000"),
            Category(id=faker.uuid4(), name="Science", color="#00ff00"),
        ]
        self.category_repository.list.return_value = categories
        result = self.usecase.execute()
        assert result == categories
        self.category_repository.list.assert_called_once()

    def test__should_return_empty_list_when_no_categories(self):
        self.category_repository.list.return_value = []
        result = self.usecase.execute()
        assert result == []
        self.category_repository.list.assert_called_once()
