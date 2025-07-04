

from typing import Container

from backend.core.category.domain.repositories.category_repository import CategoryRepositoryInterface
from backend.core.publication.domain.repositories.publication_repository import PublicationRepositoryInterface
from backend.core.thought.domain.repositories.thought_repository import ThoughtRepositoryInterface

from backend.infra.databases.relational.repositories.category_repository import CategoryRepository
from backend.infra.databases.relational.repositories.publication_repository import PublicationRepository
from backend.infra.databases.relational.repositories.thought_repository import ThoughtRepository


def setup_di_container():
    """
    Solves core dependencies by injecting concrete implementations
    """
    Container.register(CategoryRepositoryInterface, CategoryRepository)
    Container.register(ThoughtRepositoryInterface, ThoughtRepository)
    Container.register(PublicationRepositoryInterface, PublicationRepository)
