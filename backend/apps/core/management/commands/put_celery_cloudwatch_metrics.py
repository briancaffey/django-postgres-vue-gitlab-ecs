import os

import redis

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.core import celery_app
import boto3


class Command(BaseCommand):
    help = "Creates a default superuser for local development"

    def active_and_reserved_tasks_by_queue_name(self, queue_name):
        """
        i.active() returns a dictionary where keys are worker names
        and values are lists of active tasks for the worker

        """
        i = celery_app.control.inspect()

        active = i.active()
        active_count = 0
        if active:
            for _, active_tasks in active.items():
                active_count += len(
                    [
                        task
                        for task in active_tasks
                        if task['delivery_info']['routing_key'] == queue_name
                    ]
                )

        reserved = i.reserved()
        reserved_count = 0
        if reserved:
            for _, reserved_tasks in reserved.items():
                reserved_count += len(
                    [
                        task
                        for task in reserved_tasks
                        if task['delivery_info']['routing_key'] == queue_name
                    ]
                )

        r = redis.Redis(
            host=settings.REDIS_SERVICE_HOST,
            port=6379,
            db=1,
            charset="utf-8",
            decode_responses=True,
        )

        queue_length = r.llen("default")

        return active_count + reserved_count + queue_length

    def publish_queue_metrics(self, queue_names):
        metric_data = {
            queue_name: self.active_and_reserved_tasks_by_queue_name(
                queue_name
            )
            for queue_name in queue_names
        }
        if not settings.DEBUG:
            client = boto3.client('cloudwatch')
            client.put_metric_data(
                Namespace=os.environ.get("FULL_APP_NAME", "FULL_APP_NAME"),
                MetricData=[
                    {"MetricName": metric_name, "Value": value}
                    for metric_name, value in metric_data.items()
                ],
            )

    def handle(self, *args, **options):

        self.publish_queue_metrics(["default"])
