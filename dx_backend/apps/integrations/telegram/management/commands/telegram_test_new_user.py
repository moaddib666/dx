import random
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from apps.client.models import Client


class Command(BaseCommand):
    help = 'Create a test user to trigger the new user registration Telegram notification'

    def add_arguments(self, parser):
        parser.add_argument(
            '--first-name',
            type=str,
            default='Test',
            help='First name for the test user (default: Test)'
        )
        parser.add_argument(
            '--last-name',
            type=str,
            default='User',
            help='Last name for the test user (default: User)'
        )
        parser.add_argument(
            '--provider',
            type=str,
            choices=['google', 'openai', 'local'],
            default='google',
            help='Provider for the test user (default: google)'
        )

    def handle(self, *args, **options):
        # Check if Telegram is configured
        try:
            token = settings.INTEGRATION.get("telegram", {}).get("token")
            chat_id = settings.INTEGRATION.get("telegram", {}).get("chat_id")
            
            if not token:
                self.stdout.write(self.style.WARNING(
                    "⚠ Telegram token is not configured. "
                    "The user will be created but no notification will be sent."
                ))
            
            if not chat_id:
                self.stdout.write(self.style.WARNING(
                    "⚠ Telegram chat_id is not configured. "
                    "The user will be created but no notification will be sent."
                ))
        except (AttributeError, KeyError):
            self.stdout.write(self.style.WARNING(
                "⚠ Telegram integration is not configured. "
                "The user will be created but no notification will be sent."
            ))
        
        # Get parameters
        first_name = options['first_name']
        last_name = options['last_name']
        provider = options['provider']
        
        # Generate a unique test email
        random_id = random.randint(1000, 9999)
        test_email = f'test_dimension_x_{random_id}@example.com'
        
        self.stdout.write(self.style.WARNING(f"\nCreating test user..."))
        self.stdout.write(f"  Email: {test_email}")
        self.stdout.write(f"  Name: {first_name} {last_name}")
        self.stdout.write(f"  Provider: {provider}\n")
        
        try:
            # Create the test client (this will trigger the signal)
            client = Client.objects.create_user(
                email=test_email,
                password='testpass123',
                first_name=first_name,
                last_name=last_name,
                provider=provider
            )
            
            self.stdout.write(self.style.SUCCESS(f"✓ Test user created successfully!"))
            self.stdout.write(f"  Client ID: {client.id}")
            self.stdout.write(f"  Email: {client.email}")
            
            if token and chat_id:
                self.stdout.write(self.style.SUCCESS(
                    "\n✓ Telegram notification should have been sent to your configured chat."
                ))
                self.stdout.write("  Check your Telegram group/channel to verify the notification.")
            else:
                self.stdout.write(self.style.WARNING(
                    "\n⚠ Telegram notification was NOT sent (configuration incomplete)."
                ))
                self.stdout.write("  Run 'python manage.py telegram_config' to check your configuration.")
            
            self.stdout.write(self.style.WARNING(
                f"\nNote: This is a test user with email {test_email}"
            ))
            self.stdout.write("You may want to delete it later from the admin panel or database.")
            
        except Exception as e:
            raise CommandError(f"Failed to create test user: {e}")
