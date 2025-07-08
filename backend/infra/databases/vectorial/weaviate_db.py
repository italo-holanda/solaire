import os

import weaviate

from weaviate import classes as wvc

from weaviate.classes.init import AdditionalConfig, Timeout
from weaviate.classes.config import Property, DataType


class WeaviateDB:
    def __init__(self):
        self.headers = self._get_headers()
        self.additional_config = AdditionalConfig(
            timeout=Timeout(
                init=2,
                query=60,
                insert=120,
                update=120,
                delete=120,
            )
        )

    def _get_headers(self):
        """Get headers based on environment configuration"""

        is_anonymous = os.getenv("WEAVIATE_ANONYMOUS_ACCESS")
        is_production = is_anonymous == "false"

        if is_production:
            api_key = os.getenv("WEAVIATE_API_KEY")
            if not api_key:
                raise ValueError("WEAVIATE_API_KEY env var is required")
            return {"X-OpenAI-Api-Key": api_key}
        else:
            return {"X-Ollama-BaseURL": 'http://ollama:11434'}

    def _init_thought_schema(self, client: weaviate.WeaviateClient):

        try:
            client.collections.get("Thought")
            collection_exists = True
        except:
            collection_exists = False

        if not collection_exists:
            client.collections.create(
                name="Thought",
                properties=[
                    Property(name="thought_id", data_type=DataType.TEXT),
                    Property(name="content", data_type=DataType.TEXT),
                ],
                vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_ollama(
                    api_endpoint="http://ollama:11434",
                    model="nomic-embed-text"
                ),
                generative_config=wvc.config.Configure.Generative.ollama(
                    api_endpoint="http://ollama:11434",
                    model="llama3.1:latest"
                )
            )

    def get_client(self):

        client = weaviate.connect_to_local(
            host=os.getenv("WEAVIATE_HOST", "localhost"),
            port=int(os.getenv("WEAVIATE_PORT", "8080")),
            headers=self.headers,
            additional_config=self.additional_config,
            skip_init_checks=True
        )

        self._init_thought_schema(client)

        return client
