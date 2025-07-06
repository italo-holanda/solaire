import os
import pytest
import time
from faker import Faker

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
        assert config.vectorizer_config.model["model"] == "llama2"
