from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Show current Telegram bot configuration status'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("=== Telegram Bot Configuration ===\n"))
        
        # Check token
        try:
            token = settings.INTEGRATION.get("telegram", {}).get("token")
            if token:
                # Mask token for security (show first 10 and last 5 characters)
                if len(token) > 15:
                    masked_token = f"{token[:10]}...{token[-5:]}"
                else:
                    masked_token = "***"
                self.stdout.write(self.style.SUCCESS(f"✓ Token: {masked_token}"))
            else:
                self.stdout.write(self.style.ERROR("✗ Token: Not configured"))
        except (AttributeError, KeyError):
            self.stdout.write(self.style.ERROR("✗ Token: Not configured"))
            token = None
        
        # Check chat_id
        try:
            chat_id = settings.INTEGRATION.get("telegram", {}).get("chat_id")
            if chat_id:
                self.stdout.write(self.style.SUCCESS(f"✓ Chat ID: {chat_id}"))
            else:
                self.stdout.write(self.style.ERROR("✗ Chat ID: Not configured"))
        except (AttributeError, KeyError):
            self.stdout.write(self.style.ERROR("✗ Chat ID: Not configured"))
            chat_id = None
        
        self.stdout.write("")
        
        # Provide guidance based on configuration status
        if not token:
            self.stdout.write(self.style.WARNING("⚠ Token is missing!"))
            self.stdout.write("\nTo configure the token:")
            self.stdout.write("  1. Create a bot via @BotFather on Telegram")
            self.stdout.write("  2. Copy the bot token")
            self.stdout.write("  3. Add to settings_local.py:")
            self.stdout.write("     INTEGRATION = {")
            self.stdout.write('         "telegram": {')
            self.stdout.write('             "token": "YOUR_BOT_TOKEN",')
            self.stdout.write('             "chat_id": None,')
            self.stdout.write("         }")
            self.stdout.write("     }")
        elif not chat_id:
            self.stdout.write(self.style.WARNING("⚠ Chat ID is missing!"))
            self.stdout.write("\nNext steps:")
            self.stdout.write("  1. Verify bot info: python manage.py telegram_bot_info")
            self.stdout.write("  2. Add bot to your Telegram group as admin")
            self.stdout.write("  3. Send a message in the group")
            self.stdout.write("  4. Get chat ID: python manage.py telegram_get_chat_id")
            self.stdout.write("  5. Update settings_local.py with the chat_id")
        else:
            self.stdout.write(self.style.SUCCESS("✓ Configuration looks complete!"))
            self.stdout.write("\nAvailable commands:")
            self.stdout.write("  • python manage.py telegram_bot_info       - Verify bot token")
            self.stdout.write("  • python manage.py telegram_get_chat_id    - Get chat IDs")
            self.stdout.write("  • python manage.py telegram_test_message   - Send test message")
            self.stdout.write("  • python manage.py telegram_config         - Show this status")
            self.stdout.write("\nTest your configuration:")
            self.stdout.write("  python manage.py telegram_test_message")
        
        self.stdout.write("")
