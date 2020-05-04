from .development import *  # noqa

print("loading minikube settings...")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get(  # noqa
            "POSTGRES_NAME", "kubernetes_django"
        ),
        "USER": os.environ.get(  # noqa
            "POSTGRES_USER", "postgres"
        ),
        "PASSWORD": os.environ.get(  # noqa
            "POSTGRES_PASSWORD", "postgres"
        ),
        "HOST": os.environ.get(  # noqa
            "POSTGRES_SERVICE_HOST", "postgres"
        ),
        "PORT": os.environ.get(  # noqa
            "POSTGRES_SERVICE_PORT", 5432
        ),
    }
}

# Django Channels

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [
                (
                    os.environ.get(  # noqa
                        "REDIS_SERVICE_HOST"
                    ),
                    6379,
                )
            ],
        },
    },
}

# Celery Configuration

CELERY_BROKER_URL = f"redis://{os.environ.get('REDIS_SERVICE_HOST')}/1"  # noqa
CELERY_RESULT_BACKEND = f"redis://{os.environ.get('REDIS_SERVICE_HOST')}/1"  # noqa
