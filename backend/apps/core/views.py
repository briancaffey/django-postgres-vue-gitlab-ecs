import os

from django.conf import settings
from django.http import JsonResponse
from django.views.generic import TemplateView
from rest_framework import viewsets
from rest_framework.decorators import api_view

from apps.core.tasks import debug_task, send_test_email_task, sleep_task

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


def send_test_email(request):
    send_test_email_task.delay()
    return JsonResponse({"message": "Success"})
