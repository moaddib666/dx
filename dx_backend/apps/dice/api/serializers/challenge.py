from rest_framework import serializers

from apps.dice.models import Challenge, ChallengeModifier
from apps.action.models import DiceRollResult


class DiceRollResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiceRollResult
        fields = ("dice_side", "multiplier", "outcome")
        read_only_fields = ("dice_side", "multiplier", "outcome")


class ChallengeModifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChallengeModifier
        fields = ("id", "name", "icon", "value")
        read_only_fields = ("id",)


class ChallengeGenericSerializer(serializers.ModelSerializer):
    modifiers = ChallengeModifierSerializer(many=True, read_only=True)
    outcome = DiceRollResultSerializer(read_only=True)

    class Meta:
        model = Challenge
        fields = (
            "id",
            "difficulty",
            "description",
            "dice_sides",
            "outcome",
            "stat",
            "advantage",
            "disadvantage",
            "modifiers",
        )
        read_only_fields = ("id", "outcome", "modifiers", "target")
