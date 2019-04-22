from django.urls import include, path, re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from . import views

urlpatterns = [
    re_path(
        r'^auth/obtain_token/',
        TokenObtainPairView.as_view(),
        name='api-jwt-auth'
    ),
    re_path(
        r'^auth/refresh_token/',
        TokenRefreshView.as_view(),
        name='api-jwt-refresh'
    ),
    re_path(
        r'^auth/verify_token/',
        TokenVerifyView.as_view(),
        name='api-jwt-verify'
    ),
    path(
        'users/profile/',
        views.Profile.as_view(),
        name='user-profile'
    )
]

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]
