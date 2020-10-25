import os

from django.conf import settings
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)


from .utils.celery_utils import publish_celery_metrics
from apps.core.tasks import send_test_email_task, sleep_task

r = settings.REDIS


class DebugRedis(viewsets.ViewSet):
    def get(self, request):
        count = None

        value = r.get("cached_value")

        if value:
            count = value
        return JsonResponse({"count": count})

    def post(self, request):
        new_count = int(request.data["count"])
        r.set("cached_value", new_count)
        new_count = r.get("cached_value")
        return JsonResponse({"count": new_count})

    def delete(self, request):
        r.delete("cached_value")
        return JsonResponse({"count": r.get("cached_value")})


def health_check(request):
    response = JsonResponse({"message": "OK"})
    return response


@api_view(["POST"])
def sleep_task_view(request):
    sleep_seconds = request.data.get("seconds")
    sleep_task.apply_async(
        [sleep_seconds], queue=settings.CELERY_QUEUE_DEFAULT
    )
    return JsonResponse(
        {"message": f"Sleep task submitted ({sleep_seconds} seconds)"}
    )


@api_view(["POST"])
@permission_classes([])
@authentication_classes([])
def celery_metrics(request):
    if request.data.get("celery_metrics_token") == os.environ.get(
        "CELERY_METRICS_TOKEN"
    ):
        published_celery_metrics = publish_celery_metrics()
        return JsonResponse(published_celery_metrics)
    else:
        return JsonResponse({"message": "Unauthorized"}, status=401)


def send_test_email(request):
    send_test_email_task.delay()
    return JsonResponse({"message": "Success"})
