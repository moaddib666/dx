from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.character.api.serializers.openapi import AttributeSerializer, OpenaiCharacterBioSerializer, ThePathSerializer
from apps.character.models import Character, Rank, Stat
from apps.core.models import AttributeType, GodInterventionType, GodInterventionSize
from apps.currency.api.serializers.openapi import CharacterCurrencySerializer
from apps.effects.api.serializers.openapi import ActiveEffectSerializer
from apps.game.services.character.core import CharacterService
from apps.items.api.serializers.openapi import CharacterItemSerializer
from apps.shields.api.serializers.openapi import ActiveShieldSerializer


class DetailedRankSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed Rank information.

    Includes all relevant fields from the Rank model to provide comprehensive
    information about a character's rank.
    """

    class Meta:
        model = Rank
        fields = [
            'id', 'name', 'grade', 'grade_rank', 'description',
            'experience_needed', 'additional_stat_points'
        ]
        read_only_fields = fields


class GameMasterCharacterStatSerializer(serializers.ModelSerializer):
    """
    Serialize character stats for Game Master.
    """

    class Meta:
        model = Stat
        fields = [
            'id', "name", 'additional_value', 'base_value',
        ]


class GameMasterCharacterStatsCardSerializer(serializers.ModelSerializer):
    """
    Serializer for character stats card. Used in GameMasterCharacterCard component.

    This serializer provides a compact view of character stats, suitable for displaying
    in a character stats card component.
    """
    stats = GameMasterCharacterStatSerializer(many=True, read_only=True)

    class Meta:
        model = Character
        fields = [
            'id', "stats"
        ]
        read_only_fields = fields


class GameMasterCharacterInfoSerializer(serializers.ModelSerializer):
    """
    Serializer for Game Master character information.

    This serializer provides all the necessary data for rendering a GameMasterCharacterCard component.

    Included data:
    1. Shields: Using ActiveShieldSerializer to include shields related to the character.
    2. Attributes: Using AttributeSerializer to include character attributes.
    3. Active Effects: Using ActiveEffectSerializer to include active effects on the character.
    4. Items: Using CharacterItemSerializer to include character's equipped items.
    5. Currency: Using CharacterCurrencySerializer to include character's currency information.
    6. Biography: Using OpenaiCharacterBioSerializer to include character's biographical information
       (age, gender, background, appearance, avatar).
    7. Path: Using ThePathSerializer to include character's path information (name, description, icon).
    8. Rank: Using DetailedRankSerializer to include detailed rank information
       (grade, grade_rank, description, experience_needed, etc.).

    Character Card Layout Description for Frontend Developers:
    --------------------------------------------------------

    The GameMasterCharacterCard is a vertically oriented card with the following layout:

    1. Top Section:
       - Character avatar (large, centered, from biography.avatar)
       - Character name (prominent, below avatar)
       - Character biographical details (age, gender from biography)
       - Character rank and path information (below name)
         * Rank displayed with grade, grade_rank, and name
         * Path displayed with name and icon
       - Other basic character info like organization, tags, etc.
       - Left side overlay: Active shields displayed as vertical bars or icons
         * Each shield shows its type, level, and efficiency
         * Visual indicator of shield health/status
       - Right side overlay: Active effects displayed as icons with tooltips
         * Each effect shows its type and remaining cycles
         * Visual indicator for permanent vs temporary effects

    2. Middle Section:
       - Character background and appearance information (from biography)
         * Background displayed as a collapsible text section
         * Appearance displayed as a collapsible text section

    3. Bottom Section:
       - Character attributes displayed as horizontal bars
         * Each attribute shows name, current value, and max value
         * Color-coded bars for different attribute types

    4. External Sections:
       - Bottom panel main: Inventory items displayed as a grid
         * Each item shows its icon, name, type, and quantity
         * Items grouped by type if possible
       - Bottom panel bottom: Currency information
         * Each currency type with icon and amount
         * Totals and conversions if applicable

    Responsive Design Considerations:
    - On smaller screens, the layout should adjust to maintain readability
    - Consider collapsible sections for detailed information
    - Ensure tooltips are accessible on touch devices

    Interaction Guidelines:
    - Hover on shields, effects, or items should show detailed information in alt like tooltips
    - Consider item selection for further actions (e.g., emmit event to upper components)
    - Provide visual feedback for interactive elements

    """

    attributes = serializers.SerializerMethodField()
    shields = ActiveShieldSerializer(many=True, read_only=True)
    effects = ActiveEffectSerializer(many=True, read_only=True)
    equipped_items = CharacterItemSerializer(many=True, read_only=True)
    tokens = CharacterCurrencySerializer(many=True, read_only=True)

    # Character biography information
    biography = OpenaiCharacterBioSerializer(read_only=True)

    # Character path and rank information
    path = ThePathSerializer(read_only=True)
    rank = DetailedRankSerializer(read_only=True)

    @extend_schema_field(AttributeSerializer(many=True))
    def get_attributes(self, obj):
        """
        Get character attributes using CharacterService.

        This method uses the CharacterService to get the character's attributes
        (Health, Energy, Action Points) with their current and max values.
        """
        character_service = CharacterService(obj)
        attributes = [
            character_service.get_attribute(attr_name)
            for attr_name in AttributeType
        ]
        return AttributeSerializer(attributes, many=True).data

    class Meta:
        model = Character
        exclude = [
            'created_at',
            'updated_at',
        ]


class GodInterventionSerializer(serializers.Serializer):
    """
    Serializer for God Intervention actions.

    This serializer is used for the god_intervention endpoint in GameMasterCharacterViewSet.
    It validates the data needed to create a GodIntervention object.
    """
    type = serializers.ChoiceField(choices=GodInterventionType.choices())
    size = serializers.ChoiceField(choices=GodInterventionSize.choices())
    attributes = serializers.MultipleChoiceField(choices=AttributeType.choices())
