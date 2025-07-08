import os
import weaviate

from typing import List

from backend.core.thought.domain.entities.thought import Thought
from backend.core.thought.domain.repositories.thought_vector_store import ThoughtVector
from backend.infra.databases.vectorial.weaviate_db import WeaviateDB


class ThoughtVectorStore:
    def __init__(self):
        self.db = WeaviateDB()
        self.client = self.db.get_client()
        self.vector_provider = os.getenv("VECTOR_PROVIDER", "ollama").lower()

    def create_index(self, thought: Thought) -> None:
        self.client.collections.get("Thought").data.insert(
            {
                "thought_id": thought.id,
                "content": thought.text
            }
        )

    def search_similar(thought: Thought) -> List[ThoughtVector]:
        pass

    def search_similar_by_text(thought_text: str) -> List[ThoughtVector]:
        pass

    def delete_index(thought: Thought) -> None:
        pass
