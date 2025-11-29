# Telegram Bot Integration

This Django app provides Telegram bot integration for sending notifications to Telegram groups/channels.

## Features

- Send messages to Telegram groups when specific events occur
- Automatic notification when new customers register
- Decoupled architecture using Django signals
- Configurable via environment variables or settings
- Privacy-focused: No PII (Personally Identifiable Information) exposed in notifications
- Customizable welcome image via settings

## Setup

### Quick Setup with Management Commands

The easiest way to set up the Telegram integration is using the provided management commands:

#### 1. Create a Telegram Bot

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` command and follow the instructions
3. Copy the bot token provided by BotFather

#### 2. Configure the Token

Add the token to your `settings_local.py`:

```python
INTEGRATION = {
    "telegram": {
        "token": "your_bot_token_here",
        "chat_id": None,
        "welcome_image": "https://your-image-url.com/image.jpg",  # Optional: URL for welcome notification image
    }
}
```

#### 3. Verify Bot Configuration

Run the configuration check command:

```bash
python manage.py telegram_config
```

This will show your current configuration status and guide you through the next steps.

#### 4. Verify Bot Token

Check that your bot token is valid:

```bash
python manage.py telegram_bot_info
```

This will display your bot's information (username, ID, capabilities).

#### 5. Get Your Chat ID

1. Add your bot to your Telegram group as an admin
2. Send any message in the group (e.g., "Hello bot!")
3. Run the command to fetch chat IDs:

```bash
python manage.py telegram_get_chat_id
```

This will display all available chats where your bot has received messages.

#### 6. Update Configuration with Chat ID

Copy the chat ID from the previous step and update your `settings_local.py`:

```python
INTEGRATION = {
    "telegram": {
        "token": "your_bot_token_here",
        "chat_id": "-1001234567890",  # Your actual chat ID
        "welcome_image": "https://your-image-url.com/image.jpg",  # Optional: URL for welcome notification image
    }
}
```

#### 7. Test the Configuration

Send a test message to verify everything works:

```bash
python manage.py telegram_test_message
```

If successful, you should see the test message in your Telegram group!

### Alternative Setup (Manual)

You can also configure using environment variables:

```bash
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
export TELEGRAM_CHAT_ID="your_chat_id_here"
export TELEGRAM_WELCOME_IMAGE="https://your-image-url.com/image.jpg"  # Optional
```

## Configuration Options

The Telegram integration supports the following configuration options in `settings.INTEGRATION["telegram"]`:

- **`token`** (required): Your Telegram bot token from BotFather
- **`chat_id`** (required): The chat/group ID where notifications will be sent
- **`welcome_image`** (optional): URL of the image to display in new user registration notifications. If not set, notifications will be sent without an image.

### Privacy & Security

The integration is designed with privacy in mind:
- **No PII in notifications**: User email addresses and other personally identifiable information are never included in Telegram notifications
- **Minimal logging**: Logs use client IDs instead of email addresses
- **Clean formatting**: Notifications use minimal emojis for professional appearance

## Management Commands

The integration provides several management commands to help you configure and test your Telegram bot:

### `telegram_config`

Show the current configuration status and get guidance on next steps.

```bash
python manage.py telegram_config
```

**Output:**
- Current token status (masked for security)
- Current chat_id status
- Contextual guidance based on configuration state

### `telegram_bot_info`

Verify your bot token and display bot information.

```bash
python manage.py telegram_bot_info
```

**Output:**
- Bot ID
- Bot username
- Bot display name
- Bot capabilities (can join groups, read messages, etc.)

### `telegram_get_chat_id`

Fetch recent updates and extract chat IDs from conversations.

```bash
python manage.py telegram_get_chat_id [--limit N]
```

**Options:**
- `--limit N`: Number of recent updates to fetch (default: 10)

**Output:**
- List of all chats where the bot has received messages
- Chat ID, type, title, and username for each chat
- Instructions on how to configure the chat_id

**Prerequisites:**
- Bot must be added to the group as an admin
- At least one message must be sent in the group

### `telegram_test_message`

Send a test message to verify your configuration.

```bash
python manage.py telegram_test_message [--chat-id CHAT_ID] [--message "Custom message"]
```

**Options:**
- `--chat-id CHAT_ID`: Override the chat_id from settings (useful for testing different chats)
- `--message "text"`: Custom message to send (default: test message)

**Examples:**

```bash
# Send test message to configured chat
python manage.py telegram_test_message

# Send test message to specific chat
python manage.py telegram_test_message --chat-id "-1001234567890"

# Send custom message
python manage.py telegram_test_message --message "Hello from production!"
```

### `telegram_test_new_user`

Create a test user to trigger the new user registration Telegram notification.

```bash
python manage.py telegram_test_new_user [--first-name NAME] [--last-name NAME] [--provider PROVIDER]
```

**Options:**
- `--first-name NAME`: First name for the test user (default: Test)
- `--last-name NAME`: Last name for the test user (default: User)
- `--provider PROVIDER`: Provider for the test user - choices: google, openai, local (default: google)

**Output:**
- Creates a test user with a randomly generated email
- Triggers the new user registration signal
- Sends the welcome notification to your configured Telegram chat
- Displays the created user information

**Examples:**

```bash
# Create test user with default values
python manage.py telegram_test_new_user

# Create test user with custom name
python manage.py telegram_test_new_user --first-name "John" --last-name "Doe"

# Create test user with specific provider
python manage.py telegram_test_new_user --first-name "Alice" --provider "openai"
```

**Note:** This command creates actual user records in the database. You may want to delete test users later from the admin panel.

## Usage

### Automatic Notifications

The app automatically sends notifications for the following events:

- **New Customer Registration**: When a new client registers via `ClientManager.create_user()`

### Manual Usage

You can also use the Telegram service directly in your code:

```python
from apps.integrations.telegram.services import TelegramBotService

# Initialize the service
telegram = TelegramBotService()

# Send a simple message
telegram.send_message(
    chat_id="your_chat_id",
    text="Hello from Django!"
)

# Send a formatted notification
telegram.send_notification(
    chat_id="your_chat_id",
    title="Important Update",
    message="Something important happened!"
)
```

## Adding New Event Notifications

To add notifications for other events, create a new signal handler in `signals.py`:

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.integrations.telegram.services import TelegramBotService

@receiver(post_save, sender=YourModel)
def notify_your_event(sender, instance, created, **kwargs):
    if not created:
        return
    
    telegram = TelegramBotService()
    telegram.send_notification(
        chat_id=settings.INTEGRATION["telegram"]["chat_id"],
        title="Your Event Title",
        message=f"Event details: {instance}"
    )
```

## Architecture

- **services.py**: Contains `TelegramBotService` for interacting with Telegram Bot API
- **signals.py**: Django signal handlers that trigger notifications
- **apps.py**: App configuration that auto-loads signals

## Error Handling

The integration is designed to fail gracefully:

- If the token is not configured, a warning is logged and no messages are sent
- If the chat_id is not configured, notifications are skipped
- Network errors are caught and logged without breaking the application flow
- Notification failures do not affect the main application logic (e.g., user registration still succeeds)

## Testing

To test the integration without actually sending messages, you can temporarily modify the `send_message` method to log instead of sending, or use a test chat ID.

## Dependencies

The integration uses the `requests` library to communicate with the Telegram Bot API. Make sure it's installed:

```bash
pip install requests
```

## API Reference

### TelegramBotService

#### `send_message(chat_id, text, parse_mode="HTML", disable_notification=False)`

Send a message to a Telegram chat.

**Parameters:**
- `chat_id` (str): Telegram chat ID
- `text` (str): Message text
- `parse_mode` (str, optional): "HTML", "Markdown", or None
- `disable_notification` (bool, optional): Send silently

**Returns:** `bool` - True if successful

#### `send_notification(chat_id, title, message)`

Send a formatted notification with a title and message.

**Parameters:**
- `chat_id` (str): Telegram chat ID
- `title` (str): Notification title (will be bold)
- `message` (str): Notification message

**Returns:** `bool` - True if successful
