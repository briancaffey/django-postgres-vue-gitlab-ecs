"""
This command allows for daphne to be reloaded when project
code is saved. This command is called in
`docker-compose.dev.yml` and is only for use in development

https://avilpage.com/2017/05/how-to-auto-reload-celery-workers-in-development.html
"""

import shlex
import subprocess

from django.core.management.base import BaseCommand
from django.utils import autoreload


def restart_daphne():
    cmd = "pkill -9 daphne"
    subprocess.call(shlex.split(cmd))
    cmd = "daphne backend.asgi:application --bind 0.0.0.0 --port 9000"  # noqa
    subprocess.call(shlex.split(cmd))


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Starting daphne server with autoreload...")
        autoreload.run_with_reloader(restart_daphne)
