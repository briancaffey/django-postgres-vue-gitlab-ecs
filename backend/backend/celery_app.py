import os

from celery import Celery

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'backend.settings'
)

from django.conf import settings # noqa | needs to be after os env


app = Celery('backend')
app.config_from_object(
    'django.conf:settings',
    namespace='CELERY'
)

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
