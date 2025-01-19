# serializers.py
from rest_framework import serializers

from apps.core.models import ImpactType, ImpactViolationType
from ...models import CharacterAction, ActionImpact, SpecialAction


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


class RegisterCharacterActionSerializer(serializers.Serializer):
    initiator = serializers.UUIDField()
    targets = serializers.ListField(child=serializers.UUIDField())
    action_type = serializers.CharField()
    skill = serializers.UUIDField()
    data = serializers.JSONField()
    position = serializers.JSONField()


class CharacterActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterAction
        fields = ['id', 'initiator', 'targets', 'action_type', 'skill', 'data', 'position', "item"]
        read_only_fields = ['created_at', 'updated_at', "initiator"]
        extra_kwargs = {
            'targets': {'required': False},
            'skill': {'required': False},
            'item': {'required': False},
            'id': {'read_only': True},
        }


class GameMasterCharacterActionSerializer(CharacterActionSerializer):
    class Meta(CharacterActionSerializer.Meta):
        read_only_fields = ['created_at', 'updated_at']


class SpecialActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialAction
        fields = "__all__"
