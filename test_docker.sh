#!/bin/bash
docker run --rm \
  -v "$(pwd)":/app \
  -w /app \
  python:3.11-slim \
  bash -c '
    pip install --disable-pip-version-check -q pytest 2>&1 | grep -v WARNING
    pytest_output=$(python -m pytest tests/test_core.py -v 2>&1)
    pytest_exit=$?
    echo "$pytest_output" | tail -50
    exit $pytest_exit
  '
