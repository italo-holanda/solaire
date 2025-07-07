import os
import pytest
import time
from faker import Faker

from backend.core.thought.domain.entities.thought import Thought
from backend.infra.databases.vectorial.thought_vector_store import ThoughtVectorStore


faker = Faker()


class TestThoughtVectorStore:
    """Integration tests for ThoughtVectorStore using real Weaviate and Ollama connections"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test fixtures with real connections"""
        self.original_env = os.environ.copy()
        self.vector_store = ThoughtVectorStore()
        time.sleep(1)

    def teardown_method(self):
        """Cleanup after each test"""
        os.environ.clear()
        os.environ.update(self.original_env)

        try:
            if self.vector_store._collection_exists("Thought"):
                self.vector_store.client.collections.delete("Thought")
        except Exception:
            # Ignore cleanup errors
            pass

    def test__should_connect_with_db(self):
        """Test initialization with real Weaviate connection"""
        assert hasattr(self.vector_store, 'client')
        assert hasattr(self.vector_store, 'vector_provider')
        assert self.vector_store.vector_provider == 'ollama'

    def test__should_check_schema_existence(self):
        """Test _collection_exists with real schema"""
        exists = self.vector_store._collection_exists("Thought")
        assert isinstance(exists, bool)

    def test__should_create_schema_with_ollama_provider(self):
        """Test _create_schema with real ollama vector provider"""
        self.vector_store._create_schema()
        assert self.vector_store._collection_exists("Thought")

        collection = self.vector_store.client.collections.get("Thought")
        config = collection.config.get()

        assert collection is not None
        assert config.vectorizer_config.vectorizer == "text2vec-ollama"
        assert config.vectorizer_config.model["model"] == os.getenv("OLLAMA_MODEL")

    def test__should_create_new_thought_index(self):
        """Test .create_index() method"""

        thought = Thought(
            title="My weekend in Estonia",
            text="""
                Tallinn's Old Town felt like stepping into a fairytale—cobbled streets,
                medieval towers, and cozy cafés. Took a ferry to Saaremaa island, where
                the peaceful nature and windmills totally reset my mind. Tried smoked 
                fish and local beer—both amazing. Locals were friendly, though reserved.
                Loved the mix of Nordic calm and Eastern European charm. Would go back
                in a heartbeat. Estonia's small, but it packs a surprising punch.
            """,
            summary="""
                Weekend in Estonia: medieval Tallinn, peaceful Saaremaa, great food, 
                friendly vibes, unforgettable trip.
            """,
            categories=[],
            embeddings=[]
        )
        self.vector_store.create_index(thought)
