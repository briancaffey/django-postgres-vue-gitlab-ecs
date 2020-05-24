from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r"^ws/ping-pong/$", consumers.CoreConsumer),
    # url(r'^ws/chat/(?P<room_name>[^/]+)/$', consumers.CoreConsumer),
]
