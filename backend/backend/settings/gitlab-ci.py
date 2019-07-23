"""
Settings file for GitLab CI

This file inherits from `backend/backend/settings.py`
"""

from .base import * # noqa

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS # noqa

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'postgres',
        'PORT': '5432',
    },
}

STATIC_URL = '/static/'

STATIC_ROOT = '/static/'
