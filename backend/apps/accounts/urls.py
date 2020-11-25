from django.urls import include, path, re_path

from . import views


urlpatterns = [
    path("login-set-cookie/", views.login_set_cookie, name="login-view"),
    path("login/", views.login_view, name="login-view"),
    path("logout/", views.logout_view, name="logout-view"),
    path("users/profile/", views.Profile.as_view(), name="user-profile",),
    # Social Auth Callbacks
    path("social/<backend>/", views.exchange_token, name="social-auth",),
]

urlpatterns += [
    path("api-auth/", include("rest_framework.urls")),
]
