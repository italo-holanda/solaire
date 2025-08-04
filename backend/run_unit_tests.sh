#!/bin/bash

PROJECT_ROOT="src"

export PYTHONPATH="${PROJECT_ROOT}:${PYTHONPATH}"

pytest -vv --tb=short --ignore=src/infra "$@"  

