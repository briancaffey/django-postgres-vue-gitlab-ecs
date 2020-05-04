from django.urls import path

from . import views

urlpatterns = [
    path(
        "transactions/",
        views.TransactionViewSet.as_view({"get": "get"}),
        name="transactions",
    ),
    path(
        "statements/",
        views.StatementViewSet.as_view(
            {"get": "get", "post": "post"}
        ),
        name="statements",
    ),
]
