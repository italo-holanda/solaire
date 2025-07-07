#!/bin/bash

# Integration test runner for ThoughtVectorStore
# This script runs tests that require real Weaviate and Ollama connections



echo "Starting integration tests for ThoughtVectorStore..."

if [ -f .env ]; then
  set -a
  source .env
  set +a
  echo "Loaded environment variables from .env file."
else
  echo ".env file not found. Using default environment variables."
fi

echo "Environment:"
echo "  VECTOR_PROVIDER: $VECTOR_PROVIDER"
echo "  OLLAMA_MODEL: $OLLAMA_MODEL"
echo "  WEAVIATE_HOST: $WEAVIATE_HOST"
echo "  WEAVIATE_PORT: $WEAVIATE_PORT"
echo "  OLLAMA_BASE_URL: $OLLAMA_HEALTH_URL"
echo ""

# Check if services are running
echo "Checking if required services are running..."

# Check Weaviate
if curl -s "$WEAVIATE_HOST:$WEAVIATE_PORT/v1/.well-known/ready" > /dev/null; then
    echo "✓ Weaviate is running on localhost:8080"
else
    echo "✗ Weaviate is not running on $WEAVIATE_HOST:$WEAVIATE_PORT"
    echo "Please start Weaviate using: docker-compose up weaviate"
    exit 1
fi

# Check Ollama
if curl -s "$OLLAMA_HEALTH_URL/api/tags" > /dev/null; then
    echo "✓ Ollama is running on $OLLAMA_HEALTH_URL"
else
    echo "✗ Ollama is not running on $OLLAMA_HEALTH_URL"
    echo "Please start Ollama using: docker-compose up ollama"
    exit 1
fi





# Run the specific test file
#!/bin/bash

PROJECT_ROOT="backend"

export PYTHONPATH="${PROJECT_ROOT}:${PYTHONPATH}"

pytest -vv --tb=short --ignore=backend/core "$@"  

echo "Integration tests completed!" 