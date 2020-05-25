from django.urls import path

from . import views

urlpatterns = [
    path("health-check/", views.health_check, name="health-check"),
    path("celery/sleep-task/", views.sleep_task_view, name="sleep-task"),
    path(
        "debug/send-test-email/",
        views.send_test_email,
        name="send-test-email",
    ),
    path(
        "debug/redis/",
        views.DebugRedis.as_view(
            {"get": "get", "post": "post", "delete": "delete"}
        ),
        name="debug-redis",
    ),
]
