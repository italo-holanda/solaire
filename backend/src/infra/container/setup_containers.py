from src.core.publication.domain.services.publication_content_generator import PublicationContentGeneratorInterface
from src.core.publication.domain.services.publication_outlining_generator import PublicationOutliningGeneratorInterface
from src.core.thought.domain.entities.thought import Thought
from src.core.thought.domain.repositories.thought_vector_store import ThoughtVectorStoreInterface
from src.core.thought.domain.repositories.thought_repository import ThoughtRepositoryInterface
from src.core.thought.domain.services.thought_interpreter import ThoughtInterpreterInterface
from src.core.thought.domain.services.thought_topic_suggester import ThoughtTopicSuggesterInterface
from src.core.category.domain.repositories.category_repository import CategoryRepositoryInterface
from src.core.publication.domain.repositories.publication_repository import PublicationRepositoryInterface
from src.infra.container.container import Container
from src.infra.databases.relational.repositories.thought_repository import ThoughtRepository
from src.infra.databases.relational.repositories.category_repository import CategoryRepository
from src.infra.databases.relational.repositories.publication_repository import PublicationRepository
from src.infra.databases.vectorial.thought_vector_store import ThoughtVectorStore
from src.infra.agents.publication_content_generator_agent import PublicationContentGeneratorAgent
from src.infra.agents.publication_outlining_generator_agent import PublicationOutliningGeneratorAgent
from src.infra.agents.thought_interpreter_agent import ThoughtInterpreterAgent
from src.infra.agents.thought_topic_suggester_agent import ThoughtTopicSuggesterAgent


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
