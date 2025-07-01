from pydantic import BaseModel

from backend.core.domain.entities.publication import Publication, PublicationFormat
from backend.core.domain.repositories.publication_repository import PublicationRepository
from backend.core.domain.repositories.thought_repository import ThoughtRepository
from backend.core.domain.services.publication_content_generator import PublicationContentGenerator
from backend.core.domain.services.publication_title_generator import PublicationTitleGenerator


class CreatePublicationContentDTO(BaseModel):
    publication_id: str
    publication_outlining: str


class CreatePublicationContentUsecase ():
    def __init__(
        self,
        thought_repository: ThoughtRepository,
        publication_repository: PublicationRepository,
        content_generator: PublicationContentGenerator,
        title_generator: PublicationTitleGenerator
    ):
        self.thought_repository = thought_repository
        self.publication_repository = publication_repository
        self.content_generator = content_generator
        self.title_generator = title_generator

    def execute(self, dto: CreatePublicationContentDTO) -> Publication:

        publication = self.publication_repository.get_by_id(dto.publication_id)

        if not publication:
            raise ValueError("Publication not found")

        thoughts = []
        for thought_id in publication.thought_ids:
            thought = self.thought_repository.get_by_id(thought_id)
            if thought:
                thoughts.append(thought)

        content = self.content_generator.generate(
            thoughts,
            dto.user_guideline,
            outlining=publication.outlining
        )

        publication.title = self.content_generator.generate(content)
        publication.content = content
        publication.stage = "ready"

        self.publication_repository.update(publication)

        return publication
