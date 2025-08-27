from rest_framework import serializers

from apps.character.models import Character
from apps.core.models import CharacterStats
from apps.dice.models import Challenge


class GameMasterCreateChallengeSerializer(serializers.Serializer):
    """
    Serializer for GameMaster challenge creation requests.
    
    This serializer handles the data needed to create a challenge for a character,
    including target selection, dice configuration, difficulty, and modifiers.
    """
    target_character = serializers.PrimaryKeyRelatedField(
        queryset=Character.objects.filter(is_active=True),
        help_text="The character who will face this challenge"
    )
    difficulty = serializers.IntegerField(
        min_value=1,
        max_value=999,
        help_text="Difficulty Class (DC) for the challenge"
    )
    dice_sides = serializers.IntegerField(
        default=20,
        min_value=4,
        max_value=100,
        help_text="Number of sides on the dice (default: 20)"
    )
    stat = serializers.ChoiceField(
        choices=CharacterStats.choices(),
        default=CharacterStats.LUCK,
        help_text="Character stat to use for the challenge"
    )
    advantage = serializers.BooleanField(
        default=False,
        help_text="Whether the character has advantage on this challenge"
    )
    disadvantage = serializers.BooleanField(
        default=False,
        help_text="Whether the character has disadvantage on this challenge"
    )
    description = serializers.CharField(
        max_length=1000,
        required=False,
        allow_blank=True,
        help_text="Optional description of the challenge"
    )
    modifiers = serializers.ListField(
        child=serializers.DictField(
            child=serializers.UUIDField()
        ),
        required=False,
        help_text="List of modifiers to apply to the challenge"
    )

    def validate(self, data):
        """Validate the challenge data."""
        # Ensure advantage and disadvantage are not both True
        if data.get('advantage') and data.get('disadvantage'):
            raise serializers.ValidationError(
                "A challenge cannot have both advantage and disadvantage"
            )

        # Validate target character is not already in a challenge
        target_character = data.get('target_character')
        if target_character and hasattr(target_character, 'challenge') and target_character.challenge:
            raise serializers.ValidationError(
                f"Character '{target_character.name}' already has an active challenge"
            )

        return data

    def validate_target_character(self, value):
        """Validate the target character."""
        if not value.is_active:
            raise serializers.ValidationError("Cannot create challenge for inactive character")

        if value.npc:
            raise serializers.ValidationError("Cannot create challenge for NPC characters")

        return value


class GameMasterChallengeResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        read_only_fields = (
            "id",
            "difficulty",
            "description",
            "dice_sides",
            "outcome",
            "stat",
            "advantage",
            "disadvantage",
            "modifiers",
            "target",
        )
        fields = read_only_fields
        depth = 1
