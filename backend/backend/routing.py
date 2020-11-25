from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import apps.core.routing

application = ProtocolTypeRouter(
    {
        # Empty for now (http->django views is added by default)
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(apps.core.routing.websocket_urlpatterns)
        ),
    }
)
