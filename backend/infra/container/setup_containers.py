from backend.core.thought.domain.repositories.thought_vector_store import ThoughtVectorStoreInterface
from backend.core.thought.domain.services.thought_interpreter import ThoughtInterpreterInterface
from backend.infra.agents.thought_interpreter_agent import ThoughtInterpreterAgent
from backend.infra.container.container import Container

from backend.core.category.domain.repositories.category_repository import CategoryRepositoryInterface
from backend.core.publication.domain.repositories.publication_repository import PublicationRepositoryInterface
from backend.core.thought.domain.repositories.thought_repository import ThoughtRepositoryInterface

from backend.infra.databases.relational.repositories.category_repository import CategoryRepository
from backend.infra.databases.relational.repositories.publication_repository import PublicationRepository
from backend.infra.databases.relational.repositories.thought_repository import ThoughtRepository
from backend.infra.databases.vectorial.thought_vector_store import ThoughtVectorStore


def setup_di_container():
    """
    Solves core dependencies by injecting concrete implementations
    """
    Container.register(CategoryRepositoryInterface, CategoryRepository)
    Container.register(ThoughtRepositoryInterface, ThoughtRepository)
    Container.register(PublicationRepositoryInterface, PublicationRepository)
    Container.register(ThoughtVectorStoreInterface, ThoughtVectorStore)
    Container.register(ThoughtInterpreterInterface, ThoughtInterpreterAgent)
