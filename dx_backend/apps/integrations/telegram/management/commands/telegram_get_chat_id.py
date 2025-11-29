import requests
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    help = 'Get chat IDs from recent Telegram bot updates'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            default=10,
            help='Number of recent updates to fetch (default: 10)'
        )

    def handle(self, *args, **options):
        try:
            token = settings.INTEGRATION["telegram"]["token"]
            if not token:
                raise CommandError("Telegram token is not configured in settings.INTEGRATION['telegram']['token']")
        except (AttributeError, KeyError):
            raise CommandError("Telegram token is not configured in settings.INTEGRATION['telegram']['token']")

        limit = options['limit']
        url = f"https://api.telegram.org/bot{token}/getUpdates"
        params = {'limit': limit}
        
        self.stdout.write(self.style.WARNING(f"Fetching last {limit} updates from Telegram API..."))
        self.stdout.write(self.style.WARNING("(Make sure you've sent a message in your group with the bot)\n"))
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            
            if not result.get("ok"):
                raise CommandError(f"API returned error: {result.get('description', 'Unknown error')}")
            
            updates = result.get("result", [])
            
            if not updates:
                self.stdout.write(self.style.WARNING("No updates found!"))
                self.stdout.write("\nTo get your chat ID:")
                self.stdout.write("  1. Make sure the bot is added to your group as an admin")
                self.stdout.write("  2. Send any message in the group")
                self.stdout.write("  3. Run this command again")
                return
            
            self.stdout.write(self.style.SUCCESS(f"Found {len(updates)} update(s):\n"))
            
            chats_found = {}
            
            for update in updates:
                # Try to extract chat from various update types
                chat = None
                
                # Check all possible update types that contain chat information
                if 'message' in update:
                    chat = update['message'].get('chat')
                elif 'edited_message' in update:
                    chat = update['edited_message'].get('chat')
                elif 'channel_post' in update:
                    chat = update['channel_post'].get('chat')
                elif 'edited_channel_post' in update:
                    chat = update['edited_channel_post'].get('chat')
                elif 'my_chat_member' in update:
                    chat = update['my_chat_member'].get('chat')
                elif 'chat_member' in update:
                    chat = update['chat_member'].get('chat')
                
                if chat:
                    chat_id = chat.get('id')
                    chat_type = chat.get('type')
                    chat_title = chat.get('title', chat.get('first_name', 'N/A'))
                    
                    if chat_id and chat_id not in chats_found:
                        chats_found[chat_id] = {
                            'type': chat_type,
                            'title': chat_title,
                            'username': chat.get('username', 'N/A')
                        }
            
            if chats_found:
                self.stdout.write(self.style.SUCCESS("Available chats:\n"))
                
                for chat_id, info in chats_found.items():
                    self.stdout.write(f"  Chat ID: {chat_id}")
                    self.stdout.write(f"    Type: {info['type']}")
                    self.stdout.write(f"    Title: {info['title']}")
                    if info['username'] != 'N/A':
                        self.stdout.write(f"    Username: @{info['username']}")
                    self.stdout.write("")
                
                self.stdout.write(self.style.WARNING("To configure a chat ID:"))
                self.stdout.write("  1. Copy the Chat ID from above")
                self.stdout.write("  2. Add it to your settings_local.py:")
                self.stdout.write("     INTEGRATION = {")
                self.stdout.write('         "telegram": {')
                self.stdout.write('             "token": "your_token",')
                self.stdout.write('             "chat_id": "PASTE_CHAT_ID_HERE",')
                self.stdout.write("         }")
                self.stdout.write("     }")
                self.stdout.write("\n  3. Test with: python manage.py telegram_test_message")
            else:
                self.stdout.write(self.style.WARNING("No chat information found in updates"))
                
        except requests.exceptions.RequestException as e:
            raise CommandError(f"Failed to connect to Telegram API: {e}")
        except Exception as e:
            raise CommandError(f"Unexpected error: {e}")
