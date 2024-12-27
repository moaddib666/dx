# serializers.py
from rest_framework import serializers

from apps.core.models import ImpactType, ImpactViolationType
from ...models import CharacterAction, ActionImpact


class CharacterLogActionImpactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActionImpact
        exclude = ['created_at', 'updated_at', 'action']
        depth = 1
        extra_kwargs = {
            'id': {'read_only': True},
        }


class CharacterActionLogSerializer(serializers.ModelSerializer):
    impacts = CharacterLogActionImpactSerializer(many=True, read_only=True)

    class Meta:
        model = CharacterAction
        fields = [
            'id',
            'initiator',
            'targets',
            'action_type',
            'skill',
            'data',
            'position',
            'impacts',
            'cycle',
            'accepted',
            'performed',
        ]
        read_only_fields = ['created_at', 'updated_at', "initiator"]
        depth = 1
        extra_kwargs = {
            'targets': {'required': False},
            'skill': {'required': False},
            'id': {'read_only': True},
        }


class RegisterImpactActionSerializer(serializers.Serializer):
    initiator = serializers.UUIDField()
    target = serializers.UUIDField()
    impact_type = serializers.ChoiceField(choices=ImpactType.choices())
    impact_violation = serializers.ChoiceField(choices=ImpactViolationType.choices())


class CharacterActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterAction
        fields = ['id', 'initiator', 'targets', 'action_type', 'skill', 'data', 'position']
        read_only_fields = ['created_at', 'updated_at', "initiator"]
        extra_kwargs = {
            'targets': {'required': False},
            'skill': {'required': False},
            'id': {'read_only': True},
        }
