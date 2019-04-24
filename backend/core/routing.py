from django.conf.urls import url

from .consumers import CoreConsumer

websocket_urlpatterns = [
    url(r'^ws/chat/(?P<room_name>[^/]+)/$', CoreConsumer),
]
