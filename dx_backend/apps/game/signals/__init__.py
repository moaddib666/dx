from django.db.models.signals import post_save

from apps.character.models import Character
from apps.core.bus import event_bus
from apps.game.services.notifier.base import BaseNotifier

notifier = BaseNotifier(event_bus)


def on_character_changed(sender, instance, created, **kwargs):
    notifier.character_changed(instance)


post_save.connect(on_character_changed, sender=Character)
