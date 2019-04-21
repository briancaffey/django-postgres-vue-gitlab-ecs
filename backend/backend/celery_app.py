import os

from celery import Celery
from django.conf import settings # noqa | needs to be after os env

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'backend.settings'
)

app = Celery('backend')
app.config_from_object(
    'django.conf:settings',
    namespace='CELERY'
)

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
