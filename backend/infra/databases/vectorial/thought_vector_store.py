import os
import weaviate.classes.query as wq

from typing import List

from backend.core.thought.domain.entities.thought import Thought
from backend.core.thought.domain.repositories.thought_vector_store import ThoughtVector
from backend.infra.databases.vectorial.weaviate_db import WeaviateDB


class ThoughtVectorStore:
    def __init__(self):
        self.db = WeaviateDB()
        self.vector_provider = os.getenv("VECTOR_PROVIDER", "ollama").lower()

    def create_index(self, thought: Thought) -> None:
        client = self.db.get_client()
        client.collections.get("Thought").data.insert(
            {
                "thought_id": thought.id,
                "content": thought.text
            }
        )
        client.close()

    def search_similar(self, thought: Thought) -> List[ThoughtVector]:
        client = self.db.get_client()

        collection = client.collections.get("Thought")

        response = collection.query.near_text(
            query=thought.text,
            limit=5,
            return_metadata=wq.MetadataQuery(distance=True),
            return_properties=["thought_id", "content"]
        )
        results = []
        for obj in response.objects:
            results.append(
                ThoughtVector(
                    thought_id=obj.properties["thought_id"],
                    embeddings=[]
                )
            )

        client.close()
        return results

    def search_similar_by_text(self, thought_text: str) -> List[ThoughtVector]:
        client = self.db.get_client()

        collection = client.collections.get("Thought")

        response = collection.query.near_text(
            query=thought_text,
            limit=5,
            return_metadata=wq.MetadataQuery(distance=True),
            return_properties=["thought_id", "content"]
        )
        results = []
        for obj in response.objects:
            results.append(
                ThoughtVector(
                    thought_id=obj.properties["thought_id"],
                    embeddings=[]
                )
            )

        client.close()
        return results

    def delete_index(self, thought: Thought) -> None:
        client = self.db.get_client()
        collection = client.collections.get("Thought")
        collection.data.delete_many(
            where=wq.Filter.by_property("thought_id").equal(thought.id)
        )
        client.close()
