import os
from dataclasses import dataclass
from typing import List

import weaviate
from backend.core.thought.domain.entities.thought import Thought
from backend.core.thought.domain.repositories.thought_vector_store import ThoughtVector
from backend.infra.databases.vectorial.weaviate_db import WeaviateDB


class ThoughtVectorStore:
    def __init__(self):
        self.db = WeaviateDB()
        self.client = self.db.get_client()
        self.vector_provider = os.getenv("VECTOR_PROVIDER", "ollama").lower()

        if not self._collection_exists("Thought"):
            self._create_schema()

    def _collection_exists(self, class_name: str) -> bool:
        try:
            # Check if the collection exists using the new API
            self.client.collections.get(class_name)
            return True
        except Exception:
            return False

    def _create_schema(self) -> None:
        if self.vector_provider == "openai":
            vectorizer = "text2vec-openai"
            module_config = {
                "text2vec-openai": {
                    "model": os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
                }
            }
        elif self.vector_provider == "ollama":
            vectorizer = "text2vec-ollama"
            module_config = {
                "text2vec-ollama": {
                    "model": os.getenv("OLLAMA_MODEL", "llama2")
                }
            }
        else:
            raise ValueError(
                f"Unknown VECTOR_PROVIDER: {self.vector_provider}")

        # Create collection using the new API
        if self.vector_provider == "ollama":
            vectorizer_config = weaviate.classes.config.Configure.Vectorizer.text2vec_ollama(
                model=os.getenv("OLLAMA_MODEL", "llama2")
            )
        elif self.vector_provider == "openai":
            vectorizer_config = weaviate.classes.config.Configure.Vectorizer.text2vec_openai(
                model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
            )
        else:
            raise ValueError(f"Unknown VECTOR_PROVIDER: {self.vector_provider}")

        self.client.collections.create(
            name="Thought",
            vectorizer_config=vectorizer_config,
            properties=[
                weaviate.classes.config.Property(name="thought_id", data_type=weaviate.classes.config.DataType.TEXT),
                weaviate.classes.config.Property(name="text", data_type=weaviate.classes.config.DataType.TEXT)
            ]
        )

    def create_index(self, thought: Thought) -> None:
        self.client.collections.get("Thought").data.insert(
            {
                "thought_id": thought.id,
                "text": thought.text
            }
        )

    def search_similar(thought: Thought) -> List[ThoughtVector]:
        pass

    def search_similar_by_text(thought_text: str) -> List[ThoughtVector]:
        pass

    def delete_index(thought: Thought) -> None:
        pass
