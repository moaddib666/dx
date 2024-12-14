import uuid

from rest_framework import serializers

from apps.core.models import AttributeType
from apps.player.models import Player


class OpenaiCharacterSerializer(serializers.ModelSerializer):

    def validate_age(self, value):
        if not (18 <= value <= 200):
            raise serializers.ValidationError("Age must be between 18 and 200.")
        return value

    class Meta:
        model = Player
        fields = ['id', 'name', 'age', 'gender']


class CharacterStatsSerializer(serializers.Serializer):
    health = serializers.IntegerField()
    max_health = serializers.IntegerField()
    energy = serializers.IntegerField()
    max_energy = serializers.IntegerField()
    ap = serializers.IntegerField()
    max_ap = serializers.IntegerField()


class LocationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)


class RankSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    experience = serializers.IntegerField()
    next_rank_experience = serializers.IntegerField()


class AttributeSerializer(serializers.Serializer):
    name = serializers.ChoiceField(choices=[attr for attr in AttributeType])
    current = serializers.IntegerField()
    max = serializers.IntegerField()


class PlayerInfoSerializer(serializers.Serializer):
    id = serializers.UUIDField(default=uuid.uuid4)
    name = serializers.CharField(max_length=100)
    rank_grade = serializers.IntegerField()
    attributes = AttributeSerializer(many=True)
    dimension = serializers.IntegerField()
    location = serializers.UUIDField()
    fight = serializers.UUIDField()
    duel_invitations = serializers.ListField(child=serializers.UUIDField())


class PlayerPathSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['path']
