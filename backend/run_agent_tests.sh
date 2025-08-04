#!/bin/bash

# Test LLM functions

echo "Starting agents (LLM's) tests..."

echo "----------------------------------------------"
echo "⚠️ - [WARNING!] - THIS MAY TAKE A LONG TIME ⌛️"
echo "----------------------------------------------"

if [ -f .env ]; then
  set -a
  source .env
  set +a
  echo "Loaded environment variables from .env file."
else
  echo ".env file not found. Using default environment variables."
fi

echo "Environment:"
echo "  OLLAMA_MODEL: $OLLAMA_MODEL"
echo "  OLLAMA_LOCAL_URL: $OLLAMA_LOCAL_URL"
echo ""

PROJECT_ROOT="src"

export PYTHONPATH="${PROJECT_ROOT}:${PYTHONPATH}"

pytest -vv src/infra/agents "$@"  

echo "Agent tests completed!" 