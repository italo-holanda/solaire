from typing import List, Optional
from pydantic import BaseModel

from src.core.publication.domain.entities.publication import Publication
from src.core.publication.domain.repositories.publication_repository import PublicationRepositoryInterface


class ListPublicationsDTO(BaseModel):
    search_term: Optional[str] = None # Not yet necessary 


class ListPublicationsUsecase:
    def __init__(
        self,
        publication_repository: PublicationRepositoryInterface
    ):
        self.publication_repository = publication_repository

    def execute(self, _: ListPublicationsDTO = ListPublicationsDTO()) -> List[Publication]:
        return self.publication_repository.list()
