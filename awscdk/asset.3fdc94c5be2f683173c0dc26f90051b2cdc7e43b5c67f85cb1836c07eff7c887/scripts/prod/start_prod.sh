#!/bin/bash

gunicorn -t 300 -b 0.0.0.0:8000 backend.wsgi
