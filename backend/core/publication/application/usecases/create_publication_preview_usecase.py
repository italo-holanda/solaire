from typing import List
from pydantic import BaseModel

from backend.core.common.domain.exceptions.application_exception import ApplicationException
from backend.core.publication.domain.entities.publication import Publication, PublicationFormat
from backend.core.publication.domain.repositories.publication_repository import PublicationRepositoryInterface
from backend.core.publication.domain.services.publication_outlining_generator import PublicationOutliningGenerator
from backend.core.thought.domain.repositories.thought_repository import ThoughtRepositoryInterface


class CreatePublicationPreviewDTO(BaseModel):
    selected_thought_ids: List[str]
    publication_format: PublicationFormat
    user_guideline: str


class CreatePublicationPreviewUsecase ():
    def __init__(
        self,
        thought_repository: ThoughtRepositoryInterface,
        publication_repository: PublicationRepositoryInterface,
        outlining_generator: PublicationOutliningGenerator
    ):
        self.thought_repository = thought_repository
        self.publication_repository = publication_repository
        self.outlining_generator = outlining_generator

    def execute(self, dto: CreatePublicationPreviewDTO) -> Publication:

        thoughts = []
        for thought_id in dto.selected_thought_ids:
            thought = self.thought_repository.get_by_id(thought_id)
            if thought:
                thoughts.append(thought)

        if len(thoughts) == 0:
            raise ApplicationException("No thoughts found", 404)

        outlining = self.outlining_generator.generate(
            thoughts,
            dto.user_guideline
        )

        saved = self.publication_repository.save(
            Publication(
                title=f"Preview - {outlining[0]}",
                content="",
                categories=[],
                format=dto.publication_format,
                stage="preview",
                outlining=outlining,
                thought_ids=dto.selected_thought_ids,
                user_guideline=dto.user_guideline
            )
        )

        return saved
