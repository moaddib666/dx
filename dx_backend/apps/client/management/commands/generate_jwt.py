from django.core.management.base import BaseCommand
from rest_framework_simplejwt.tokens import RefreshToken

from apps.client.models import Client
from apps.game.models import Campaign


class Command(BaseCommand):
    help = "Generate JWT token for clients with various filtering options"

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            help="Email of the specific client to generate token for (optional)"
        )
        parser.add_argument(
            '--id',
            type=int,
            help="ID of the specific client to generate token for (optional)"
        )
        parser.add_argument(
            '--admin',
            action='store_true',
            help="Filter for admin clients only (is_superuser=True)"
        )
        parser.add_argument(
            '--is_active',
            type=bool,
            default=True,
            help="Filter by active status (default: True)"
        )
        parser.add_argument(
            '--campaign',
            type=int,
            help="Filter clients by their main character's campaign ID (optional)"
        )

    def handle(self, *args, **kwargs):
        email = kwargs.get('email')
        client_id = kwargs.get('id')
        is_admin = kwargs.get('admin', False)
        is_active = kwargs.get('is_active', True)
        campaign_id = kwargs.get('campaign')

        # Build the filter dictionary
        filters = {'is_active': is_active}

        if email:
            filters['email'] = email

        if client_id:
            filters['id'] = client_id

        if is_admin:
            filters['is_superuser'] = True

        # Get clients based on filters
        clients = Client.objects.filter(**filters)

        # Additional filter for campaign if provided
        if campaign_id:
            try:
                campaign = Campaign.objects.get(id=campaign_id)
                # Filter clients whose main character is in the specified campaign
                clients = clients.filter(main_character__campaign=campaign)
            except Campaign.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f"Campaign with ID {campaign_id} does not exist")
                )
                return

        if not clients.exists():
            self.stdout.write(
                self.style.WARNING("No clients found matching the specified criteria")
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
