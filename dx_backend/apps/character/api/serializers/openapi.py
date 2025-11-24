import uuid

from rest_framework import serializers

from apps.action.models import DiceRollResult
from apps.character.models import Character, CharacterBiography, Stat, Rank, PublishedCharacter
from apps.core.models import AttributeType, GenderEnum
from apps.game.models import Campaign
from apps.school.models import ThePath


class OpenaiCharacterBioSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterBiography
        fields = "__all__"

    def to_representation(self, instance):
        """
        Custom representation to handle avatar URLs.
        Uses request from context to build absolute URLs for avatar.
        """
        representation = super().to_representation(instance)

        # Handle avatar URL to make it absolute if request is available
        if representation.get('avatar') and self.context.get('request'):
            representation['avatar'] = self.context.get('request').build_absolute_uri(representation['avatar'])

        return representation


class PublishedCharacterSerializer(serializers.ModelSerializer):
    biography = OpenaiCharacterBioSerializer(read_only=True)
    character_name = serializers.SerializerMethodField()
    
    class Meta:
        model = PublishedCharacter
        fields = ['id', 'character_name', 'biography', 'big_avatar', 'small_avatar', 'tiktok_link', 'youtube_link', 'instagram_link', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_character_name(self, obj):
        """
        Retrieve the character name from the related biography and character.
        Returns None if biography or character is not available.
        """
        if obj.biography and obj.biography.character:
            return obj.biography.character.name
        return None
    
    def to_representation(self, instance):
        """
        Custom representation to handle avatar URLs.
        Uses request from context to build absolute URLs for avatars.
        """
        representation = super().to_representation(instance)
        
        # Handle big_avatar URL to make it absolute if request is available
        if representation.get('big_avatar') and self.context.get('request'):
            representation['big_avatar'] = self.context.get('request').build_absolute_uri(representation['big_avatar'])
        
        # Handle small_avatar URL to make it absolute if request is available
        if representation.get('small_avatar') and self.context.get('request'):
            representation['small_avatar'] = self.context.get('request').build_absolute_uri(representation['small_avatar'])
        
        return representation


class ThePathSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThePath
        fields = ['name', 'description', "icon", "id"]


class RankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rank
        fields = ['name', 'grade', 'experience_needed']


class CampaignSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)

    class Meta:
        model = Campaign
        fields = ['id', 'name']


class OrganizationSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)


class OpenaiCharacterSerializer(serializers.ModelSerializer):
    biography = OpenaiCharacterBioSerializer()
    rank = RankSerializer()
    path = ThePathSerializer()
    campaign = CampaignSerializer()
    organization = OrganizationSerializer(allow_null=True)
    position_id = serializers.UUIDField(allow_null=True)

    def validate_age(self, value):
        if not (18 <= value <= 200):
            raise serializers.ValidationError("Age must be between 18 and 200.")
        return value

    class Meta:
        model = Character
        fields = [
            'id',
            'name',
            'biography',
            "npc",
            "rank",
            "path",
            "experience",
            "tags",
            "resetting_base_stats",
            "is_active",
            "campaign",
            "fight",
            "challenge",
            "organization",
            "position_id",
        ]


class CharacterAttrsSerializer(serializers.Serializer):
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


class CharacterInfoSerializer(serializers.Serializer):
    id = serializers.UUIDField(default=uuid.uuid4)
    name = serializers.CharField(max_length=100)
    rank_grade = serializers.IntegerField()
    attributes = AttributeSerializer(many=True)
    dimension = serializers.IntegerField()
    location = serializers.UUIDField()
    fight = serializers.UUIDField(allow_null=True)


class StatModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stat
        exclude = ['created_at', 'updated_at', "character"]


class StatSerializer(serializers.Serializer):
    name = serializers.CharField()
    value = serializers.IntegerField()


class CharacterStatsSerializer(serializers.ModelSerializer):
    stats = StatSerializer(many=True)

    class Meta:
        model = Character
        fields = ['stats']


class CharacterPathSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ['path']


class BioSerializer(serializers.Serializer):
    age = serializers.IntegerField()
    gender = serializers.ChoiceField(choices=["Male", "Female", "Other"])
    appearance = serializers.CharField(max_length=5000)
    background = serializers.CharField(max_length=5000)
    avatar = serializers.ImageField(allow_null=True, required=False)


class ModificatorSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()


class ItemSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    type = serializers.CharField()


class SchoolSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    level = serializers.IntegerField()


class SpellSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    school = serializers.UUIDField()
    level = serializers.IntegerField()


class CharacterTemplateSerializer(serializers.Serializer):
    name = serializers.CharField()
    tags = serializers.ListField(child=serializers.CharField(), default=[])
    bio = BioSerializer()
    rank = serializers.IntegerField()
    path = serializers.UUIDField(allow_null=True)
    stats = StatSerializer(many=True, default=[])
    modificators = serializers.ListField(child=serializers.UUIDField(), default=[])
    items = serializers.ListField(child=serializers.UUIDField(), default=[])
    schools = serializers.ListField(child=serializers.UUIDField(), default=[])
    spells = serializers.ListField(child=serializers.UUIDField(), default=[])


class CharacterTemplateValidationSerializer(serializers.Serializer):
    max_stats_points_count = serializers.IntegerField()
    max_modificators_count = serializers.IntegerField()
    max_items_count = serializers.IntegerField()
    max_spells_count = serializers.IntegerField()
    max_rank_grade = serializers.IntegerField()
    max_schools_count = serializers.IntegerField()


class CharacterTemplateFullSerializer(serializers.Serializer):
    id = serializers.UUIDField(allow_null=True, default=None)
    data = CharacterTemplateSerializer()
    validation = CharacterTemplateValidationSerializer()


class CharacterBioDraftSerializer(serializers.Serializer):
    age = serializers.IntegerField(min_value=18, max_value=900)
    gender = serializers.ChoiceField(choices=GenderEnum.choices())
    appearance = serializers.CharField(max_length=5000, allow_blank=True)
    background = serializers.CharField(max_length=5000, allow_blank=True)


class CharacterStatSerializer(serializers.Serializer):
    name = serializers.CharField()
    value = serializers.IntegerField()


class CharacterGenericDataSerializer(serializers.Serializer):
    name = serializers.CharField()
    tags = serializers.ListField(child=serializers.CharField())
    bio = CharacterBioDraftSerializer()
    rank = serializers.IntegerField()
    path = serializers.UUIDField()
    stats = CharacterStatSerializer(many=True)
    modificators = serializers.ListField(child=serializers.UUIDField())
    items = serializers.ListField(child=serializers.UUIDField())
    schools = serializers.ListField(child=serializers.UUIDField())
    spells = serializers.ListField(child=serializers.IntegerField())


class DiceRollResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiceRollResult
        fields = ['dice_side', ]


class DetailStatSerializer(serializers.ModelSerializer):
    dice_rolls = DiceRollResultSerializer(many=True)

    class Meta:
        model = Stat
        exclude = ['created_at', 'updated_at']


class SwipeBaseStatSerializer(serializers.Serializer):
    from_stat = serializers.UUIDField(
        help_text="The first result of the base stat generation."
    )
    to_stat = serializers.UUIDField(
        help_text="The second result of the base stat generation.",
    )

    def validate(self, attrs):
        if attrs["from_stat"] == attrs["to_stat"]:
            raise serializers.ValidationError("The stats must be different.")
        return attrs
