import pytest
from unittest.mock import Mock
from faker import Faker

from backend.core.common.domain.exceptions.application_exception import ApplicationException
from core.publication.application.usecases.create_publication_preview_usecase import (
    CreatePublicationPreviewDTO, CreatePublicationPreviewUsecase
)
from core.publication.domain.entities.publication import Publication
from core.thought.domain.entities.thought import Thought

faker = Faker()


class TestCreatePublicationPreviewUsecase:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.dependencies = {
            "thought_repository": Mock(),
            "publication_repository": Mock(),
            "outlining_generator": Mock(),
        }
        self.usecase = CreatePublicationPreviewUsecase(
            thought_repository=self.dependencies["thought_repository"],
            publication_repository=self.dependencies["publication_repository"],
            outlining_generator=self.dependencies["outlining_generator"]
        )

    """
    1. Should create the publication preview successfully
    2. Should throw error when missing thoughts
    3. Should correctly call the outlining generator
    """

    def test__should_create_publication_preview_successfully(self):

        thought_ids = [faker.uuid4(), faker.uuid4()]
        thoughts = [Mock(spec=Thought), Mock(spec=Thought)]
        outlining = ["Section 1", "Section 2"]
        publication_format = "blog_post"
        user_guideline = "Be concise."

        for _ in zip(thought_ids, thoughts):
            self.dependencies["thought_repository"] \
                .get_by_id.side_effect = lambda x: thoughts[thought_ids.index(x)] \
                if x in thought_ids else None

        self.dependencies["outlining_generator"].generate.return_value = outlining

        publication = Publication(
            id=faker.uuid4(),
            title=f"Preview - {outlining[0]}",
            content="",
            categories=[],
            outlining=outlining,
            format=publication_format,
            stage="preview",
            thought_ids=thought_ids,
            user_guideline=user_guideline
        )
        self.dependencies["publication_repository"].save.return_value = publication

        dto = CreatePublicationPreviewDTO(
            selected_thought_ids=thought_ids,
            publication_format=publication_format,
            user_guideline=user_guideline
        )

        result = self.usecase.execute(dto)

        assert result.title == f"Preview - {outlining[0]}"
        assert result.format == publication_format
        assert result.stage == "preview"
        assert result.outlining == outlining
        assert result.thought_ids == thought_ids

        self.dependencies["publication_repository"] \
            .save.assert_called_once()

        self.dependencies["outlining_generator"] \
            .generate.assert_called_once_with(thoughts, user_guideline)

    def test__should_throw_error_when_missing_thoughts(self):
        thought_ids = [faker.uuid4(), faker.uuid4()]
        self.dependencies["thought_repository"].get_by_id.return_value = None
        dto = CreatePublicationPreviewDTO(
            selected_thought_ids=thought_ids,
            publication_format="blog_post",
            user_guideline="Any guideline"
        )

        with pytest.raises(ApplicationException, match="No thoughts found"):
            self.usecase.execute(dto)

        calls = [((tid,),) for tid in thought_ids]
        actual_calls = self.dependencies["thought_repository"].get_by_id.call_args_list

        for call in calls:
            assert call in actual_calls

    def test__should_correctly_call_outlining_generator(self):
        thought_ids = [faker.uuid4(), faker.uuid4()]
        thoughts = [Mock(spec=Thought), Mock(spec=Thought)]

        for _ in zip(thought_ids, thoughts):
            self.dependencies["thought_repository"] \
                .get_by_id.side_effect = lambda x: thoughts[
                    thought_ids.index(x)
            ] if x in thought_ids else None

        self.dependencies["outlining_generator"] \
            .generate.return_value = ["Section 1"]

        self.dependencies["publication_repository"] \
            .save.return_value = Mock(spec=Publication)

        dto = CreatePublicationPreviewDTO(
            selected_thought_ids=thought_ids,
            publication_format="blog_post",
            user_guideline="Guide"
        )

        self.usecase.execute(dto)

        self.dependencies["outlining_generator"] \
            .generate.assert_called_once_with(thoughts, "Guide")
