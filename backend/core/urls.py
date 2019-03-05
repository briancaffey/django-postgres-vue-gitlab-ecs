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
]
