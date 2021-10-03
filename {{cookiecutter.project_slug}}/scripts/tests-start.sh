#! /usr/bin/env bash
set -e

python /app/app/backend_pre_start.py

bash ./app/scripts/test.sh "$@"
