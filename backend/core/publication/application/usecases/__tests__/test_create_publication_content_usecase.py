import pytest
from unittest.mock import Mock
from faker import Faker

from backend.core.common.domain.exceptions.application_exception import ApplicationException
from core.publication.application.usecases.create_publication_content_usecase import (
    CreatePublicationContentDTO, CreatePublicationContentUsecase
)
from core.publication.domain.entities.publication import Publication
from core.thought.domain.entities.thought import Thought

faker = Faker()


class TestCreatePublicationContentUsecase:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.dependencies = {
            "thought_repository": Mock(),
            "publication_repository": Mock(),
            "content_generator": Mock(),
            "title_generator": Mock(),
        }
        self.usecase = CreatePublicationContentUsecase(
            thought_repository=self.dependencies["thought_repository"],
            publication_repository=self.dependencies["publication_repository"],
            content_generator=self.dependencies["content_generator"],
            title_generator=self.dependencies["title_generator"]
        )

    """
    1. Should create the publication content successfully
    2. Should throw error when publication not found
    """

    def test__should_create_publication_content_successfully(self):
        publication_id = faker.uuid4()
        thought_ids = [faker.uuid4(), faker.uuid4()]
        thoughts = [Mock(spec=Thought), Mock(spec=Thought)]

        publication = Mock(spec=Publication)
        publication.thought_ids = thought_ids
        publication.outlining = "Some outlining"
        publication.user_guideline = "Be clear."

        self.dependencies["publication_repository"].get_by_id.return_value = publication
        self.dependencies["thought_repository"]. \
            get_by_id.side_effect = lambda x: thoughts[
                thought_ids.index(x)
        ] if x in thought_ids else None

        content = "Generated content"
        title = "Generated title"

        self.dependencies["content_generator"] \
            .generate.side_effect = [content, title]

        dto = CreatePublicationContentDTO(
            publication_id=publication_id,
            publication_outlining="Some outlining"
        )
        result = self.usecase.execute(dto)

        assert result == publication
        assert publication.content == content
        assert publication.title == title
        assert publication.stage == "ready"

        self.dependencies["publication_repository"].update \
            .assert_called_once_with(publication)
        self.dependencies["content_generator"].generate \
            .assert_any_call(
                thoughts,
                publication.user_guideline,
                outlining=publication.outlining
        )

    def test__should_raise_error_when_publication_not_found(self):
        publication_id = faker.uuid4()
        self.dependencies["publication_repository"].get_by_id.return_value = None
        dto = CreatePublicationContentDTO(
            publication_id=publication_id,
            publication_outlining="Some outlining"
        )
        with pytest.raises(ApplicationException, match="Publication not found"):
            self.usecase.execute(dto)
        self.dependencies["publication_repository"].get_by_id \
            .assert_called_once_with(publication_id)
