#!/bin/bash

PROJECT_ROOT="backend"

export PYTHONPATH="${PROJECT_ROOT}:${PYTHONPATH}"

pytest -vv --tb=short --ignore=backend/infra "$@"  

