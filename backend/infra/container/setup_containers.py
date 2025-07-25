from backend.core.publication.domain.services.publication_content_generator import PublicationContentGeneratorInterface
from backend.core.publication.domain.services.publication_outlining_generator import PublicationOutliningGeneratorInterface
from backend.core.thought.domain.entities.thought import Thought
from backend.core.thought.domain.repositories.thought_vector_store import ThoughtVectorStoreInterface
from backend.core.thought.domain.repositories.thought_repository import ThoughtRepositoryInterface
from backend.core.thought.domain.services.thought_interpreter import ThoughtInterpreterInterface
from backend.core.thought.domain.services.thought_topic_suggester import ThoughtTopicSuggesterInterface
from backend.core.category.domain.repositories.category_repository import CategoryRepositoryInterface
from backend.core.publication.domain.repositories.publication_repository import PublicationRepositoryInterface
from backend.infra.container.container import Container
from backend.infra.databases.relational.repositories.thought_repository import ThoughtRepository
from backend.infra.databases.relational.repositories.category_repository import CategoryRepository
from backend.infra.databases.relational.repositories.publication_repository import PublicationRepository
from backend.infra.databases.vectorial.thought_vector_store import ThoughtVectorStore
from backend.infra.agents.publication_content_generator_agent import PublicationContentGeneratorAgent
from backend.infra.agents.publication_outlining_generator_agent import PublicationOutliningGeneratorAgent
from backend.infra.agents.thought_interpreter_agent import ThoughtInterpreterAgent
from backend.infra.agents.thought_topic_suggester_agent import ThoughtTopicSuggesterAgent


def setup_di_container():
    """
    Solves core dependencies by injecting concrete implementations
    """

    # Repositories
    Container.register(
        CategoryRepositoryInterface,
        CategoryRepository
    )
    Container.register(
        ThoughtRepositoryInterface,
        ThoughtRepository
    )
    Container.register(
        PublicationRepositoryInterface,
        PublicationRepository
    )
    Container.register(
        ThoughtVectorStoreInterface,
        ThoughtVectorStore
    )

    # Agents
    Container.register(
        ThoughtInterpreterInterface,
        ThoughtInterpreterAgent
    )
    Container.register(
        ThoughtTopicSuggesterInterface,
        ThoughtTopicSuggesterAgent
    )
    Container.register(
        PublicationOutliningGeneratorInterface,
        PublicationOutliningGeneratorAgent
    )
    Container.register(
        PublicationContentGeneratorInterface,
        PublicationContentGeneratorAgent
    )
