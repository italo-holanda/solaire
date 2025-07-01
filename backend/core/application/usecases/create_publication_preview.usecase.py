from typing import List
from pydantic import BaseModel

from backend.core.domain.entities.publication import Publication, PublicationFormat
from backend.core.domain.repositories.publication_repository import PublicationRepository
from backend.core.domain.repositories.thought_repository import ThoughtRepository
from backend.core.domain.services.publication_outlining_generator import PublicationOutliningGenerator


class CreatePublicationPreviewDTO(BaseModel):
    selected_thought_ids: List[str]
    publication_format: PublicationFormat
    user_guideline: str


class CreatePublicationPreviewUsecase ():
    def __init__(
        self,
        thought_repository: ThoughtRepository,
        publication_repository: PublicationRepository,
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

        outlining = self.outlining_generator.generate(
            thoughts,
            dto.user_guideline
        )

        saved = self.publication_repository.save(
            Publication(
                title=f"Preview - {outlining[0]}",
                outlining=outlining
            )
        )

        return saved
