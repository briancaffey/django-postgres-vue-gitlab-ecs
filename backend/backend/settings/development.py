from .base import *  # noqa

SECRET_KEY = "my-secret-key"

# Celery

CELERY_BROKER_URL = os.environ.get(  # noqa
    "CELERY_BROKER_URL", "redis://redis:6379"
)  # noqa
CELERY_RESULT_BACKEND = os.environ.get(  # noqa
    "CELERY_RESULT_BACKEND", "redis://redis:6379"
)  # noqa

DEBUG_APPS = ["django_extensions", "debug_toolbar"]

INSTALLED_APPS += DEBUG_APPS  # noqa

MIDDLEWARE = [
    "apps.core.middleware.healthchecks.HealthCheckMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
] + MIDDLEWARE  # noqa


def show_toolbar(request):
    return True


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": show_toolbar,
}

log_level = "DEBUG"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",  # noqa
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv(  # noqa
                "DJANGO_LOG_LEVEL", "INFO"
            ),  # noqa
        },
        "portal": {
            "handlers": ["console"],
            "level": os.getenv(  # noqa
                "PORTAL_LOG_LEVEL", log_level
            ),  # noqa
        },
    },
}

EMAIL_USE_TLS = False


NOTEBOOK_ARGUMENTS = [
    "--ip",
    "0.0.0.0",
    "--allow-root",
    "--no-browser",
]

AWS_ACCESS_KEY_ID = os.environ.get(  # noqa
    "AWS_ACCESS_KEY_ID", "key_id"
)  # noqa
AWS_SECRET_ACCESS_KEY = os.environ.get(  # noqa
    "AWS_SECRET_ACCESS_KEY", "key"
)  # noqa

STATIC_URL = "/static/"

STATIC_ROOT = "/static/"

MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")  # noqa
