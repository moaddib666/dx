import requests
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    help = 'Get Telegram bot information and verify token'

    def handle(self, *args, **options):
        try:
            token = settings.INTEGRATION["telegram"]["token"]
            if not token:
                raise CommandError("Telegram token is not configured in settings.INTEGRATION['telegram']['token']")
        except (AttributeError, KeyError):
            raise CommandError("Telegram token is not configured in settings.INTEGRATION['telegram']['token']")

        url = f"https://api.telegram.org/bot{token}/getMe"
        
        self.stdout.write(self.style.WARNING(f"Fetching bot info from Telegram API..."))
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get("ok"):
                bot_info = result.get("result", {})
                
                self.stdout.write(self.style.SUCCESS("\n✓ Bot token is valid!\n"))
                self.stdout.write(self.style.SUCCESS("Bot Information:"))
                self.stdout.write(f"  ID: {bot_info.get('id')}")
                self.stdout.write(f"  Username: @{bot_info.get('username')}")
                self.stdout.write(f"  First Name: {bot_info.get('first_name')}")
                self.stdout.write(f"  Can Join Groups: {bot_info.get('can_join_groups')}")
                self.stdout.write(f"  Can Read All Group Messages: {bot_info.get('can_read_all_group_messages')}")
                self.stdout.write(f"  Supports Inline Queries: {bot_info.get('supports_inline_queries')}")
                
                self.stdout.write(self.style.WARNING("\nNext steps:"))
                self.stdout.write("  1. Add this bot to your Telegram group as an admin")
                self.stdout.write("  2. Run: python manage.py telegram_get_chat_id")
                
            else:
                raise CommandError(f"API returned error: {result.get('description', 'Unknown error')}")
                
        except requests.exceptions.RequestException as e:
            raise CommandError(f"Failed to connect to Telegram API: {e}")
        except Exception as e:
            raise CommandError(f"Unexpected error: {e}")
