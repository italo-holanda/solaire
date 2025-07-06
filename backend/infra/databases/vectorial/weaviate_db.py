import os

import weaviate
from weaviate.classes.init import AdditionalConfig, Timeout


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
            return {}

    def get_client(self):
        
        self._configure_ollama_embedding()

        return weaviate.connect_to_local(
            host=os.getenv("WEAVIATE_HOST", "localhost"),
            port=int(os.getenv("WEAVIATE_PORT", "8080")),
            headers=self.headers,
            additional_config=self.additional_config
        )

    def _configure_ollama_embedding(self):
        """Configure environment variables for Ollama embedding integration"""

        os.environ.setdefault(
            "ENABLE_MODULES",
            "text2vec-ollama"
        )

        os.environ.setdefault(
            "DEFAULT_VECTORIZER_MODULE",
            "text2vec-ollama"
        )

        os.environ.setdefault(
            "OLLAMA_BASE_URL",
            os.getenv("OLLAMA_BASE_URL", "http://localhost:7869")
        )

        os.environ.setdefault(
            "OLLAMA_MODEL",
            os.getenv("OLLAMA_MODEL", "llama2")
        )

        os.environ.setdefault(
            "OLLAMA_INCLUDE_VECTOR",
            "true"
        )

        os.environ.setdefault(
            "OLLAMA_VECTOR_DIMENSION",
            "4096"
        )
