from rest_framework import serializers

from apps.core.models import BehaviorModel


class NPCBehaviorSerializer(serializers.Serializer):
    """
    Serializer for changing NPC behavior.
    """
    behavior = serializers.ChoiceField(choices=BehaviorModel.choices())