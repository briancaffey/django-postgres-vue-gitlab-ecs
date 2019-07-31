#!/bin/bash

# set -e

echo "Building services"
docker-compose -f docker-compose.ci.yml -f cypress-debug.yml build

echo "Starting Application"
docker-compose -f docker-compose.ci.yml up -d
sleep 20
echo "Services are up and ready"

# echo "Seeding database with user"
# docker-compose -f docker-compose.ci.yml exec backend python manage.py create_default_user

docker-compose -f docker-compose.ci.yml -f cypress-debug.yml up --exit-code-from cypress

echo "Cypress tests passed successfully."

echo "Stopping docker compose..."
docker-compose -f docker-compose.ci.yml -f cypress-debug.yml down
