from django.db.models.signals import post_save

from apps.character.models import Character
from apps.core.bus import event_bus
from apps.game.services.notifier.base import BaseNotifier

notifier = BaseNotifier(event_bus)


def on_character_changed(sender, instance, created, **kwargs):
    # Skip notification if this is a creation (handle separately if needed)
    if created:
        notifier.character_changed(instance)
        return

    # Check if specific fields were updated
    update_fields = kwargs.get('update_fields')
    if not update_fields:
        return
    notifier.character_changed(instance)


post_save.connect(on_character_changed, sender=Character)
