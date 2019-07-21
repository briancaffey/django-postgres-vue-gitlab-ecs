from celery import Celery
from django.conf import settings # noqa | needs to be after os env

app = Celery('backend')
app.config_from_object(
    'django.conf:settings',
    namespace='CELERY'
)

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
