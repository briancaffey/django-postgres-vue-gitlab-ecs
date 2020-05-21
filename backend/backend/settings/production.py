from .base import *  # noqa

# Email

EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get(  # noqa
    "DJANGO_EMAIL_HOST_USER", "user@gmail.com"
)  # noqa
EMAIL_HOST_PASSWORD = os.environ.get(  # noqa
    "DJANGO_EMAIL_HOST_PASSWORD", "emailpassword"
)  # noqa

# AWS S3 Static Files

STATICFILES_STORAGE = "backend.storage_backends.StaticStorage"
STATIC_URL = "/static/"
MEDIA_URL = "/media/"
FULL_DOMAIN_NAME = os.environ.get("FULL_DOMAIN_NAME", "dev.mysite.com")  # noqa
AWS_S3_CUSTOM_DOMAIN = FULL_DOMAIN_NAME

STATIC_ROOT = f"//{FULL_DOMAIN_NAME}/{STATIC_URL}/"
MEDIA_ROOT = f"//{FULL_DOMAIN_NAME}/{MEDIA_URL}/"


# Logging

log_level = "INFO"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler",},},  # noqa
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),  # noqa  # noqa
        },
        "portal": {
            "handlers": ["console"],
            "level": os.getenv("PORTAL_LOG_LEVEL", log_level),  # noqa  # noqa
        },
    },
}

# Celery

CELERY_BROKER_URL = "sqs://"  # f"redis://{REDIS_SERVICE_HOST}:6379/0"  # noqa
CELERY_BROKER_TRANSPORT_OPTIONS = {'region': 'eu-west-1'}

CELERY_RESULT_BACKEND = f"redis://{REDIS_SERVICE_HOST}:6379/0"  # noqa
