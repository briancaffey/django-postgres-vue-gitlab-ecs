"""
This command allows for celery to be reloaded when project
code is saved. This command is called in
`docker-compose.dev.yml` and is only for use in development

https://avilpage.com/2017/05/how-to-auto-reload-celery-workers-in-development.html
"""

import os
import shlex
import subprocess

from django.core.management.base import BaseCommand
from django.utils import autoreload


def restart_celery(queue=None, concurrency=None):
    cmd = 'pkill -9 celery'
    subprocess.call(shlex.split(cmd))
    cmd = f"celery worker --app=backend.celery_app:app --loglevel=info -Q {queue} -n worker-{queue}@%h --concurrency={os.environ.get('CONCURRENT_WORKERS', 2)} --max-memory-per-child=150000"  # noqa
    subprocess.call(shlex.split(cmd))


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '-q', '--queue', nargs=1, default='celery', type=str
        )
        parser.add_argument('-c', '--concurrency', type=str)

    def handle(self, *args, **options):
        queue = options['queue'][0]
        concurrency = options['concurrency'] or 1
        print('Starting celery worker with autoreload...')
        autoreload.run_with_reloader(
            restart_celery, queue=queue, concurrency=concurrency
        )
