# serializers.py
from rest_framework import serializers

from apps.core.models import AttributeType
from apps.fight.models import DuelInvitation, Fight, FightTurn, FightTurnAction
from apps.player.models import Player


class DuelInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DuelInvitation
        fields = '__all__'
        read_only_fields = ['is_accepted', 'is_rejected', 'fight', 'created_at', 'updated_at', "initiator"]


class FightMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fight
        fields = ['id', 'is_ended', "current_turn"]


class PlayerAttributeSerializer(serializers.Serializer):
    name = serializers.ChoiceField(choices=[attr for attr in AttributeType])
    current = serializers.IntegerField()
    max = serializers.IntegerField()


class FightParticipantSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    attributes = PlayerAttributeSerializer(many=True)
    dimension = serializers.IntegerField()
    rank_grade = serializers.IntegerField()


class FightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fight
        fields = '__all__'


class CurrentFightSerializer(serializers.Serializer):
    fight = FightMiniSerializer()
    allies = FightParticipantSerializer(many=True)
    enemies = FightParticipantSerializer(many=True)


class FightTurnSerializer(serializers.ModelSerializer):
    class Meta:
        model = FightTurn
        fields = '__all__'


class FightTurnActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FightTurnAction
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'initiator', "impact", "order", "is_finished", "turn", ]
