from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(
        r"^ws/ping-pong/$",
        consumers.CoreConsumer.as_asgi(),
    ),
]
