from typing import List
from pydantic import BaseModel

from src.core.common.domain.exceptions.application_exception import ApplicationException
from src.core.publication.domain.entities.publication import Publication
from src.core.publication.domain.repositories.publication_repository import PublicationRepositoryInterface
from src.core.publication.domain.services.publication_content_generator import PublicationContentGeneratorInterface
from src.core.thought.domain.repositories.thought_repository import ThoughtRepositoryInterface


class CreatePublicationContentDTO(BaseModel):
    publication_id: str
    publication_outlining: List[str]


class CreatePublicationContentUsecase ():
    def __init__(
        self,
        thought_repository: ThoughtRepositoryInterface,
        publication_repository: PublicationRepositoryInterface,
        content_generator: PublicationContentGeneratorInterface,
    ):
        self.thought_repository = thought_repository
        self.publication_repository = publication_repository
        self.content_generator = content_generator

    def execute(self, dto: CreatePublicationContentDTO) -> Publication:

        publication = self.publication_repository.get_by_id(dto.publication_id)

        if not publication:
            raise ApplicationException("Publication not found", 404)

        thoughts = []
        for thought_id in publication.thought_ids:
            thought = self.thought_repository.get_by_id(thought_id)
            if thought:
                thoughts.append(thought)

        generated = self.content_generator.invoke(
            thoughts,
            publication.user_guideline,
            outlining=dto.publication_outlining
        )

        try:
            publication.title = generated.title
            publication.content = generated.content
            publication.stage = "ready"
        except ValueError:
            raise ApplicationException('Invalid publication', 400)

        self.publication_repository.update(publication)

        return publication
