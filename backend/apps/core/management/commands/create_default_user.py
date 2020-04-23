from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = (
        "Creates a default superuser for local development"
    )

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.all():
            print("Creating default user")
            User.objects.create_superuser(
                email="admin@company.com",
                password="password",
            )
            print(
                """
                Default user created:
                email: 'admin@company.com'
                password: 'password'
                """
            )
        else:
            print("Not creating default user")
