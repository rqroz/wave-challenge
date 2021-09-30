#!/bin/bash
set -e

source .venv/bin/activate
ENVIRONMENT="test" python -m pytest tests
