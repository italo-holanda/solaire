#!/bin/bash

# Integration test runner for ThoughtVectorStore
# This script runs tests that require real Weaviate and Ollama connections

echo "Starting integration tests for ThoughtVectorStore..."

# Check if services are running
echo "Checking if required services are running..."

# Check Weaviate
if curl -s http://localhost:8080/v1/.well-known/ready > /dev/null; then
    echo "✓ Weaviate is running on localhost:8080"
else
    echo "✗ Weaviate is not running on localhost:8080"
    echo "Please start Weaviate using: docker-compose up weaviate"
    exit 1
fi

# Check Ollama
if curl -s http://localhost:7869/api/tags > /dev/null; then
    echo "✓ Ollama is running on localhost:7869"
else
    echo "✗ Ollama is not running on localhost:7869"
    echo "Please start Ollama using: docker-compose up ollama"
    exit 1
fi

# Set environment variables for testing
export VECTOR_PROVIDER=ollama
export OLLAMA_MODEL=llama2
export WEAVIATE_HOST=localhost
export WEAVIATE_PORT=8080
export OLLAMA_BASE_URL=http://localhost:7869
export WEAVIATE_ANONYMOUS_ACCESS=true

echo "Running integration tests..."
echo "Environment:"
echo "  VECTOR_PROVIDER: $VECTOR_PROVIDER"
echo "  OLLAMA_MODEL: $OLLAMA_MODEL"
echo "  WEAVIATE_HOST: $WEAVIATE_HOST"
echo "  WEAVIATE_PORT: $WEAVIATE_PORT"
echo "  OLLAMA_BASE_URL: $OLLAMA_BASE_URL"
echo ""

# Run the specific test file
python -m pytest backend/infra/databases/vectorial/test_thought_vector_store.py -v

echo "Integration tests completed!" 