"""
This command allows for celery to be reloaded when project
code is saved. This command is called in
`docker-compose.dev.yml` and is only for use in development

https://avilpage.com/2017/05/how-to-auto-reload-celery-workers-in-development.html
"""

import shlex
import subprocess

from django.core.management.base import BaseCommand
from django.utils import autoreload


def restart_celery():
    cmd = 'pkill -9 celery'
    subprocess.call(shlex.split(cmd))
    cmd = 'celery worker --app=backend.celery_app:app --loglevel=info --concurrency=2 --max-memory-per-child=150000'  # noqa
    subprocess.call(shlex.split(cmd))


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Starting celery worker with autoreload...')
        autoreload.run_with_reloader(restart_celery)
