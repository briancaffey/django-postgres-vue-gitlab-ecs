#!/bin/bash

python3 manage.py collectstatic --no-input
python3 manage.py makemigrations
python3 manage.py migrate --no-input

# this creates a default superuser if there are no users
# see backend/accounts/management/commands/create_default_user.py
python3 manage.py create_default_user
while true; do
    python3 manage.py runserver_plus 0.0.0.0:8000
    sleep 5s
done
