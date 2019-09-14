from .development import *  # noqa

print("loading minikube settings...")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_NAME', 'kubernetes_django'), # noqa
        'USER': os.environ.get('POSTGRES_USER', 'postgres'), # noqa
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'postgres'), # noqa
        'HOST': os.environ.get('POSTGRES_HOST', 'postgres'), # noqa
        'PORT': os.environ.get('POSTGRES_PORT', 5432), # noqa
    }
}
