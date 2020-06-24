#!/bin/bash

gunicorn -t 300 -k gevent -w 4 -b 0.0.0.0:8000 backend.wsgi
