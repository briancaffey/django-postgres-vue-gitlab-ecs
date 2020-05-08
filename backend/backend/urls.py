"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

urlpatterns = [
    path(
        "graphql/", csrf_exempt(GraphQLView.as_view(graphiql=settings.DEBUG)),
    ),
    path("admin/", admin.site.urls),
    path("api/", include("apps.accounts.urls")),
    path("api/", include("apps.core.urls")),
    path("api/", include("apps.banking.urls")),
]


if settings.DEBUG:
    import debug_toolbar  # noqa

    urlpatterns = (
        urlpatterns
        + [
            # path('', index_view, name='index'),
            path("admin/__debug__/", include(debug_toolbar.urls),),
            # catch all rule so that we can navigate to
            # routes in vue app other than "/"
            # re_path(r'^(?!js)(?!css)(?!statics)(?!fonts)(?!service\-worker\.js)(?!manifest\.json)(?!precache).*', index_view, name='index') # noqa
        ]
        + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT,)
        + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT,)
    )
