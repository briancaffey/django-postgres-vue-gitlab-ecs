from celery import Celery
from django.conf import (  # noqa | needs to be after os env
    settings
)

app = Celery("backend")
app.config_from_object(
    "django.conf:settings", namespace="CELERY"
)

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
