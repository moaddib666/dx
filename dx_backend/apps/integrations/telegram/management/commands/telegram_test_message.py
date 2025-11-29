from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from apps.integrations.telegram.services import TelegramBotService


class Command(BaseCommand):
    help = 'Send a test message to verify Telegram bot configuration'

    def add_arguments(self, parser):
        parser.add_argument(
            '--chat-id',
            type=str,
            help='Chat ID to send message to (overrides settings)'
        )
        parser.add_argument(
            '--message',
            type=str,
            default='🤖 Test message from Django application',
            help='Custom message to send (default: test message)'
        )

    def handle(self, *args, **options):
        # Get chat_id from argument or settings
        chat_id = options.get('chat_id')
        
        if not chat_id:
            try:
                chat_id = settings.INTEGRATION["telegram"]["chat_id"]
                if not chat_id:
                    raise CommandError(
                        "Chat ID is not configured. Either:\n"
                        "  1. Set it in settings.INTEGRATION['telegram']['chat_id'], or\n"
                        "  2. Use --chat-id argument"
                    )
            except (AttributeError, KeyError):
                raise CommandError(
                    "Chat ID is not configured. Either:\n"
                    "  1. Set it in settings.INTEGRATION['telegram']['chat_id'], or\n"
                    "  2. Use --chat-id argument"
                )
        
        message = options['message']
        
        self.stdout.write(self.style.WARNING(f"Sending test message to chat ID: {chat_id}..."))
        
        try:
            # Initialize Telegram service
            telegram_service = TelegramBotService()
            
            # Send test message
            success = telegram_service.send_notification(
                chat_id=str(chat_id),
                title="🧪 Test Notification",
                message=message
            )
            
            if success:
                self.stdout.write(self.style.SUCCESS("\n✓ Test message sent successfully!"))
                self.stdout.write("\nCheck your Telegram group/chat to verify the message was received.")
                self.stdout.write(self.style.SUCCESS("\nConfiguration is working correctly! ✓"))
            else:
                raise CommandError(
                    "Failed to send test message. Check the logs for details.\n"
                    "Common issues:\n"
                    "  - Bot is not added to the group\n"
                    "  - Bot is not an admin in the group\n"
                    "  - Chat ID is incorrect"
                )
                
        except ValueError as e:
            raise CommandError(f"Configuration error: {e}")
        except Exception as e:
            raise CommandError(f"Unexpected error: {e}")
