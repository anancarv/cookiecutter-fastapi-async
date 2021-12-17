#! /usr/bin/env bash
set -e

python /app/app/backend_pre_start.py
poetry install --no-root

bash ./app/scripts/test.sh "$@"
