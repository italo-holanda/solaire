import pytest
from unittest.mock import Mock
from faker import Faker

from backend.core.common.domain.exceptions.application_exception import ApplicationException
from backend.core.publication.application.usecases.create_publication_content_usecase import (
    CreatePublicationContentDTO, CreatePublicationContentUsecase
)
from backend.core.publication.domain.entities.publication import Publication
from backend.core.publication.domain.services.publication_content_generator import PublicationContentOutput
from backend.core.thought.domain.entities.thought import Thought
from backend.core.category.domain.entities.category import Category

faker = Faker()


class TestCreatePublicationContentUsecase:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.thought_repository = Mock()
        self.publication_repository = Mock()
        self.content_generator = Mock()
        self.usecase = CreatePublicationContentUsecase(
            thought_repository=self.thought_repository,
            publication_repository=self.publication_repository,
            content_generator=self.content_generator
        )

    def make_category(self):
        return Category(
            id=faker.uuid4(),
            name=faker.word(),
            color=faker.color_name()
        )

    def make_thought(self, id=None):
        return Thought(
            id=id or faker.uuid4(),
            title=faker.sentence(nb_words=3),
            summary=faker.sentence(nb_words=6),
            text=faker.text(max_nb_chars=200) + (" lorem ipsum" * 10),
            categories=[self.make_category() for _ in range(2)],
            embeddings=[faker.pyfloat(left_digits=1, right_digits=5)
                        for _ in range(5)]
        )

    def make_publication(self, thought_ids=None, stage="preview"):
        return Publication(
            id=faker.uuid4(),
            title=faker.sentence(nb_words=6),
            content=faker.text(max_nb_chars=200),
            categories=[self.make_category() for _ in range(2)],
            outlining=[faker.sentence() for _ in range(3)],
            format="blog_post",
            stage=stage,
            thought_ids=thought_ids or [faker.uuid4() for _ in range(2)],
            user_guideline=faker.sentence()
        )

    def test__should_create_publication_content_successfully(self):
        publication = self.make_publication()
        thoughts = [self.make_thought(id=tid)
                    for tid in publication.thought_ids]
        outlining = ["Intro", "Body", "Conclusion"]
        generated_output = PublicationContentOutput(
            title="Generated Title", content="Generated Content")

        self.publication_repository.get_by_id.return_value = publication
        self.thought_repository.get_by_id.side_effect = lambda tid: next(
            (t for t in thoughts if t.id == tid), None)
        self.content_generator.invoke.return_value = generated_output

        dto = CreatePublicationContentDTO(
            publication_id=publication.id,
            publication_outlining=outlining
        )

        result = self.usecase.execute(dto)

        assert result.title == generated_output.title
        assert result.content == generated_output.content
        assert result.stage == "ready"
        self.publication_repository.update.assert_called_once_with(publication)
        self.content_generator.invoke.assert_called_once_with(
            thoughts,
            publication.user_guideline,
            outlining=outlining
        )

    def test__should_raise_when_publication_not_found(self):
        self.publication_repository.get_by_id.return_value = None
        dto = CreatePublicationContentDTO(
            publication_id=faker.uuid4(),
            publication_outlining=["Section 1"]
        )
        with pytest.raises(ApplicationException) as exc:
            self.usecase.execute(dto)
        assert exc.value.code == 404
        assert "not found" in exc.value.message.lower()
