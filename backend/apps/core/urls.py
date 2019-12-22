from django.urls import path

from . import views

urlpatterns = [
    path(
        '',
        views.home,
        name="home"
    ),
    path(
        'hello-world',
        views.hello_world,
        name="hello-world"
    ),
    path(
        'debug-task/',
        views.debug_task_view,
        name="debug-task"
    ),
    path(
        'verify-domain/',
        views.verify_domain,
        name="verify-domain"
    ),
    path(
        'debug/send-test-email/',
        views.send_test_email,
        name="verify-domain"
    ),
    path(
        'debug/redis/',
        views.DebugRedis.as_view({
            "get": "get",
            "post": "post",
            "delete": "delete"
        }),
        name="debug-redis"
    ),

]
