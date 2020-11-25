from .development import *  # noqa

print("loading minikube settings...")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get("POSTGRES_NAME", "kubernetes_django"),  # noqa
        "USER": os.environ.get("POSTGRES_USER", "postgres"),  # noqa
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "postgres"),  # noqa
        "HOST": os.environ.get("POSTGRES_SERVICE_HOST", "postgres"),  # noqa
        "PORT": os.environ.get("POSTGRES_SERVICE_PORT", 5432),  # noqa
    }
}

# Django Channels

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [(os.environ.get("REDIS_SERVICE_HOST"), 6379,)],},  # noqa
    },
}

# Celery Configuration

CELERY_BROKER_URL = f"redis://{os.environ.get('REDIS_SERVICE_HOST')}/1"  # noqa
CELERY_RESULT_BACKEND = f"redis://{os.environ.get('REDIS_SERVICE_HOST')}/1"  # noqa
