#!/bin/bash

# Caminho do projeto (raiz onde o código começa, ex: `backend`)
PROJECT_ROOT="backend"

# Adiciona o diretório do projeto ao PYTHONPATH para evitar erros de importação
export PYTHONPATH="${PROJECT_ROOT}:${PYTHONPATH}"

# Roda pytest com os argumentos passados (se houver)
pytest -vv --tb=short "$@"  

