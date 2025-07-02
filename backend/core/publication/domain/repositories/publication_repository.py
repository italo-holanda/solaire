from abc import ABC, abstractmethod
from typing import List

from backend.core.publication.domain.entities.publication import Publication


class PublicationRepository(ABC):

    @abstractmethod
    def save(publication: Publication) -> Publication:
        pass

    @abstractmethod
    def get_by_id(id: str) -> Publication:
        pass

    @abstractmethod
    def list() -> List[Publication]:
        pass

    @abstractmethod
    def delete(id: str) -> None:
        pass

    @abstractmethod
    def update(publication: Publication) -> None:
        pass
