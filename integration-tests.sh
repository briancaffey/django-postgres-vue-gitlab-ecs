#!/bin/bash

# set -e

echo "Starting services"
docker-compose -f docker-compose.ci.yml up -d --build

sleep 20
echo "Services are up and ready"

echo "Seeding database with user"
docker-compose -f docker-compose.ci.yml exec backend python manage.py create_default_user

docker-compose -f cypress.yml up --exit-code-from cypress --build

echo "Cypress tests passed successfully."

echo "Stopping docker compose..."
docker-compose -f docker-compose.ci.yml -f cypress.yml