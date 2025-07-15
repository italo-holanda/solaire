import pytest
from unittest.mock import Mock
from faker import Faker

from backend.core.publication.application.usecases.list_publications_usecase import ListPublicationsDTO, ListPublicationsUsecase
from backend.core.publication.domain.entities.publication import Publication
from backend.core.category.domain.entities.category import Category

faker = Faker()

class TestListPublicationsUsecase:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.publication_repository = Mock()
        self.usecase = ListPublicationsUsecase(self.publication_repository)

    def make_category(self):
        return Category(
            id=faker.uuid4(),
            name=faker.word(),
            color=faker.color_name()
        )

    def make_publication(self):
        return Publication(
            id=faker.uuid4(),
            title=faker.sentence(nb_words=6),
            content=faker.text(max_nb_chars=200),
            categories=[self.make_category() for _ in range(2)],
            outlining=[faker.sentence() for _ in range(3)],
            format="blog_post",
            stage="preview",
            thought_ids=[faker.uuid4() for _ in range(2)],
            user_guideline=faker.sentence()
        )

    def test__should_return_list_of_publications(self):
        publications = [self.make_publication() for _ in range(3)]
        self.publication_repository.list.return_value = publications
        result = self.usecase.execute(ListPublicationsDTO())
        assert result == publications
        self.publication_repository.list.assert_called_once()

    def test__should_return_empty_list_when_no_publications(self):
        self.publication_repository.list.return_value = []
        result = self.usecase.execute(ListPublicationsDTO())
        assert result == []
        self.publication_repository.list.assert_called_once()
