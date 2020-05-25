from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import apps.core.routing

application = ProtocolTypeRouter(
    {
        # Empty for now (http->django views is added by default)
        "websocket": AuthMiddlewareStack(
            URLRouter(apps.core.routing.websocket_urlpatterns)
        ),
    }
)
