from django.core.management.base import BaseCommand
from rest_framework_simplejwt.tokens import RefreshToken

from apps.client.models import Client


class Command(BaseCommand):
    help = "Generate JWT token for active admin clients"

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            help="Email of the specific admin client to generate token for (optional)"
        )

    def handle(self, *args, **kwargs):
        email = kwargs.get('email')

        if email:
            # Generate token for a specific client
            try:
                client = Client.objects.get(
                    email=email,
                    is_active=True,
                    is_superuser=True  # Assuming is_staff represents admin status
                )
                self._generate_token_for_client(client)
            except Client.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f"No active admin client found with email: {email}")
                )
        else:
            # Generate tokens for all active admin clients
            clients = Client.objects.filter(
                is_active=True,
                is_superuser=True  # Assuming is_staff represents admin status
            )

            if not clients.exists():
                self.stdout.write(
                    self.style.WARNING("No active admin clients found")
                )
                return

            for client in clients:
                self._generate_token_for_client(client)

    def _generate_token_for_client(self, client):
        """Generate and display JWT token for a client."""
        refresh = RefreshToken.for_user(client)

        self.stdout.write(self.style.SUCCESS(f"JWT tokens for {client.email}:"))
        self.stdout.write("Access token:")
        self.stdout.write(str(refresh.access_token))
        self.stdout.write("Refresh token:")
        self.stdout.write(str(refresh))
