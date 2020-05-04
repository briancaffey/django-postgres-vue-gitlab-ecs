import jwt
from channels.auth import (
    AuthMiddlewareStack,
    CookieMiddleware
)
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections

User = get_user_model()


class TokenAuthMiddleware:
    """
    Token authorization middleware for Django Channels 2
    """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        close_old_connections()
        cookies = scope["cookies"]
        if "user-token" in cookies:
            token = jwt.decode(
                cookies["user-token"],
                settings.SECRET_KEY,
                algorithms=["HS256"],
                options={"verify_exp": False},
            )
            user_id = token["user_id"]
            try:
                user = User.objects.get(id=user_id)
                scope["user"] = user
            except User.DoesNotExist:
                scope["user"] = AnonymousUser()
        return self.inner(scope)


TokenAuthMiddlewareStack = lambda inner: CookieMiddleware(  # noqa
    TokenAuthMiddleware(AuthMiddlewareStack(inner))
)
