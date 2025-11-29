import logging
import requests
from typing import Optional
from django.conf import settings


logger = logging.getLogger(__name__)


class TelegramBotService:
    """
    Service for interacting with Telegram Bot API.
    Handles sending messages to Telegram groups/chats.
    """

    def __init__(self):
        """Initialize the Telegram bot service with token from settings."""
        self.token = self._get_token()
        self.base_url = f"https://api.telegram.org/bot{self.token}"

    def _get_token(self) -> str:
        """
        Get Telegram bot token from settings.
        
        Returns:
            str: Telegram bot token
            
        Raises:
            ValueError: If token is not configured in settings
        """
        try:
            token = settings.INTEGRATION["telegram"]["token"]
            if not token:
                raise ValueError("Telegram token is empty")
            return token
        except (AttributeError, KeyError) as e:
            logger.error(f"Telegram token not found in settings: {e}")
            raise ValueError(
                "Telegram token not configured. Please set settings.INTEGRATION['telegram']['token']"
            ) from e

    def send_message(
        self,
        chat_id: str,
        text: str,
        parse_mode: Optional[str] = "HTML",
        disable_notification: bool = False
    ) -> bool:
        """
        Send a message to a Telegram chat/group.
        
        Args:
            chat_id: Telegram chat ID (can be group ID, channel ID, or user ID)
            text: Message text to send
            parse_mode: Message parse mode (HTML, Markdown, or None)
            disable_notification: Send message silently
            
        Returns:
            bool: True if message was sent successfully, False otherwise
        """
        if not self.token:
            logger.error("Cannot send message: Telegram token not configured")
            return False

        url = f"{self.base_url}/sendMessage"
        
        payload = {
            "chat_id": chat_id,
            "text": text,
            "disable_notification": disable_notification,
        }
        
        if parse_mode:
            payload["parse_mode"] = parse_mode

        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            if result.get("ok"):
                logger.info(f"Message sent successfully to chat {chat_id}")
                return True
            else:
                logger.error(f"Failed to send message: {result.get('description', 'Unknown error')}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending Telegram message: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending Telegram message: {e}")
            return False

    def send_photo(
        self,
        chat_id: str,
        photo: str,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = "HTML",
        disable_notification: bool = False
    ) -> bool:
        """
        Send a photo to a Telegram chat/group.
        
        Args:
            chat_id: Telegram chat ID (can be group ID, channel ID, or user ID)
            photo: Photo to send (URL or file_id)
            caption: Photo caption (optional)
            parse_mode: Caption parse mode (HTML, Markdown, or None)
            disable_notification: Send photo silently
            
        Returns:
            bool: True if photo was sent successfully, False otherwise
        """
        if not self.token:
            logger.error("Cannot send photo: Telegram token not configured")
            return False

        url = f"{self.base_url}/sendPhoto"
        
        payload = {
            "chat_id": chat_id,
            "photo": photo,
            "disable_notification": disable_notification,
        }
        
        if caption:
            payload["caption"] = caption
        
        if parse_mode:
            payload["parse_mode"] = parse_mode

        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            if result.get("ok"):
                logger.info(f"Photo sent successfully to chat {chat_id}")
                return True
            else:
                logger.error(f"Failed to send photo: {result.get('description', 'Unknown error')}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending Telegram photo: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending Telegram photo: {e}")
            return False

    def send_notification(self, chat_id: str, title: str, message: str) -> bool:
        """
        Send a formatted notification message to a Telegram chat/group.
        
        Args:
            chat_id: Telegram chat ID
            title: Notification title
            message: Notification message
            
        Returns:
            bool: True if notification was sent successfully, False otherwise
        """
        formatted_text = f"<b>{title}</b>\n\n{message}"
        return self.send_message(chat_id, formatted_text, parse_mode="HTML")
