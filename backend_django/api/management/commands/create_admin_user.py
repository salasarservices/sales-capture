"""Management command to create admin user."""

from django.core.management.base import BaseCommand
from api.models import User


class Command(BaseCommand):
    help = "Create an admin user"

    def add_arguments(self, parser):
        parser.add_argument("--username", default="admin", help="Username")
        parser.add_argument("--password", help="Password (will prompt if not provided)")
        parser.add_argument("--role", default="admin", choices=["admin", "viewer"], help="User role")

    def handle(self, *args, **options):
        username = options["username"]
        password = options.get("password")
        role = options["role"]

        if not password:
            import getpass
            password = getpass.getpass("Enter password: ")

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            user.set_password(password)
            user.role = role
            user.is_staff = (role == "admin")
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Updated user: {username}"))
        else:
            user = User.objects.create_user(
                username=username,
                password=password,
                role=role,
                is_staff=(role == "admin"),
            )
            self.stdout.write(self.style.SUCCESS(f"Created user: {username} ({role})"))