#! /usr/bin/env bash

# Exit in case of error
set -e

docker-compose down -v --remove-orphans # Remove possibly previous broken stacks left hanging after an error

docker-compose build --build-arg INSTALL_DEV=true
docker-compose up -d
sleep 1
docker-compose exec -T api bash /app/scripts/tests-start.sh "$@"
