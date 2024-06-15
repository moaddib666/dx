# serializers.py
from rest_framework import serializers

from apps.fight.models import DuelInvitation, Fight, FightTurn, FightTurnAction


class DuelInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DuelInvitation
        fields = '__all__'
        read_only_fields = ['is_accepted', 'is_rejected', 'fight', 'created_at', 'updated_at', "initiator"]


class FightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fight
        fields = '__all__'


class FightTurnSerializer(serializers.ModelSerializer):
    class Meta:
        model = FightTurn
        fields = '__all__'


class FightTurnActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FightTurnAction
        fields = '__all__'
