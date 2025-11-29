import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from apps.client.models import Client
from apps.integrations.telegram.services import TelegramBotService


logger = logging.getLogger(__name__)


@receiver(post_save, sender=Client)
def notify_new_client_registration(sender, instance, created, **kwargs):
    """
    Send a Telegram notification when a new client registers.
    
    This signal handler is triggered after a Client instance is saved.
    It only sends a notification for newly created clients (not updates).
    
    Args:
        sender: The model class (Client)
        instance: The actual Client instance being saved
        created: Boolean indicating if this is a new record
        **kwargs: Additional keyword arguments
    """
    if not created:
        # Only notify for new registrations, not updates
        return

    try:
        # Get chat_id from settings
        chat_id = settings.INTEGRATION.get("telegram", {}).get("chat_id")
        
        if not chat_id:
            logger.warning("Telegram chat_id not configured. Skipping notification.")
            return

        # Initialize Telegram service
        telegram_service = TelegramBotService()
        
        # Prepare the name display
        full_name = f"{instance.first_name} {instance.last_name}".strip()
        if not full_name:
            full_name = "Anonymous Traveler"
        
        # Create a themed "dimension-x" message with clean formatting
        caption = (
            f"✨ <b>A NEW SOUL HAS ARRIVED TO DIMENSION-X</b>\n\n"
            f"<b>Traveler Identity:</b>\n"
            f"   • <b>Name:</b> {full_name}\n"
        )
        
        # Add provider info if available
        if instance.provider:
            caption += f"   • <b>Gateway:</b> {instance.provider.title()}\n"
        
        caption += (
            f"\n<i>Welcome to the adventure, brave soul!</i>\n"
            f"<i>Your journey through the dimensions begins now...</i>"
        )
        
        # Get image URL from settings (configurable)
        photo_url = settings.INTEGRATION.get("telegram", {}).get("welcome_image", "")
        
        # Send photo with caption
        success = telegram_service.send_photo(
            chat_id=chat_id,
            photo=photo_url,
            caption=caption,
            parse_mode="HTML"
        )
        
        if success:
            logger.info(f"Telegram notification sent for new client: {instance.id}")
        else:
            logger.error(f"Failed to send Telegram notification for client: {instance.id}")
            
    except ValueError as e:
        # Token not configured
        logger.warning(f"Telegram notification skipped: {e}")
    except Exception as e:
        # Don't let notification failures break the registration process
        logger.error(f"Error sending Telegram notification for new client {instance.id}: {e}")
