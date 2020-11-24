import os

import redis

from django.conf import settings

from apps.core import celery_app
import boto3


def active_and_reserved_tasks_by_queue_name(queue_name):
    """
    i.active() returns a dictionary where keys are worker names
    and values are lists of active tasks for the worker

    """
    print("inspecting celery queue")
    i = celery_app.control.inspect()

    active = i.active()
    active_count = 0
    if active:
        for _, active_tasks in active.items():
            active_count += len(
                [
                    task
                    for task in active_tasks
                    if task["delivery_info"]["routing_key"] == queue_name
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
                    if task["delivery_info"]["routing_key"] == queue_name
                ]
            )

    print("connecting to redis")
    r = redis.Redis(
        host=settings.REDIS_SERVICE_HOST,
        port=6379,
        db=1,
        charset="utf-8",
        decode_responses=True,
    )

    queue_length = r.llen("default")
    total = active_count + reserved_count + queue_length
    print(f"Active count: {active_count}")
    print(f"Reserved count: {reserved_count}")
    print(f"Queue length: {queue_length}")
    print(f"Total: {total}")
    return total


def publish_queue_metrics(queue_names):
    print("gathering queue data")
    metric_data = {
        queue_name: active_and_reserved_tasks_by_queue_name(queue_name)
        for queue_name in queue_names
    }
    print("sending cloudwatch data")
    if not settings.DEBUG:
        print("connecting aws api")
        client = boto3.client("cloudwatch")
        client.put_metric_data(
            Namespace=os.environ.get("FULL_APP_NAME", "FULL_APP_NAME"),
            MetricData=[
                {"MetricName": metric_name, "Value": value}
                for metric_name, value in metric_data.items()
            ],
        )
    return metric_data


def publish_celery_metrics():
    print("starting task")
    queue_metrics = publish_queue_metrics(["default"])
    return queue_metrics
