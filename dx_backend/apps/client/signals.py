from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.client.models import Client
from apps.game.models import Campaign


@receiver(post_save, sender=Client)
def add_client_to_default_campaigns(sender, instance, created, **kwargs):
    """
    Add newly created client to all default campaigns as a player and
    set client's current campaign to the first default campaign.
    If no default campaign exists, this step is skipped.
    """
    if not created:
        return

    # Get all default campaigns
    default_campaigns = Campaign.objects.filter(default=True, is_active=True)

    if not default_campaigns.exists():
        return

    # Add client to all default campaigns as a player
    for campaign in default_campaigns:
        campaign.players.add(instance)

    # Set client's current campaign to the first default campaign
    first_default_campaign = default_campaigns.first()
    if first_default_campaign:
        instance.current_campaign = first_default_campaign
        instance.save(update_fields=['current_campaign'])
