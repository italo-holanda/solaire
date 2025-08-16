#!/bin/bash

# Test LLM functions

echo "Starting agents (LLM's) tests..."

echo "----------------------------------------------"
echo "⚠️ - [WARNING!] - THIS MAY TAKE A LONG TIME ⌛️"
echo "----------------------------------------------"

root_dir="$(dirname "$(pwd)")"
env_file="$root_dir/.env"

if [ -f "$env_file" ]; then
  set -a
  source "$env_file"
  set +a
  echo "Loaded environment variables from $env_file"
else
  echo "$env_file not found. Using default environment variables."
fi

echo "Environment:"
echo "  OLLAMA_MODEL: $OLLAMA_MODEL"
echo "  OLLAMA_LOCAL_URL: $OLLAMA_LOCAL_URL"
echo ""

PROJECT_ROOT="src"

export PYTHONPATH="${PROJECT_ROOT}:${PYTHONPATH}"

pytest -vv src/infra/agents "$@"  

echo "Agent tests completed!" 