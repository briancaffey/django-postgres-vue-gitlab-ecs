#!/bin/bash

ping postgres -c 20
python3 manage.py collectstatic --no-input
sleep 20
cat /etc/hosts
python3 manage.py makemigrations
python3 manage.py migrate --no-input
python3 manage.py create_default_user
gunicorn -t 300 -b 0.0.0.0:8000 backend.wsgi
