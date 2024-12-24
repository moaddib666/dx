import uuid

from rest_framework import serializers

from apps.character.models import Character, CharacterBiography
from apps.core.models import AttributeType, GenderEnum


class OpenaiCharacterBioSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterBiography
        fields = "__all__"


class OpenaiCharacterSerializer(serializers.ModelSerializer):
    biography = OpenaiCharacterBioSerializer()

    def validate_age(self, value):
        if not (18 <= value <= 200):
            raise serializers.ValidationError("Age must be between 18 and 200.")
        return value

    class Meta:
        model = Character
        fields = ['id', 'name', 'biography']


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


class CharacterInfoSerializer(serializers.Serializer):
    id = serializers.UUIDField(default=uuid.uuid4)
    name = serializers.CharField(max_length=100)
    rank_grade = serializers.IntegerField()
    attributes = AttributeSerializer(many=True)
    dimension = serializers.IntegerField()
    location = serializers.UUIDField()
    fight = serializers.UUIDField(allow_null=True)
    duel_invitations = serializers.ListField(child=serializers.UUIDField())


class CharacterPathSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ['path']


from rest_framework import serializers


class BioSerializer(serializers.Serializer):
    age = serializers.IntegerField()
    gender = serializers.ChoiceField(choices=["Male", "Female", "Other"])
    appearance = serializers.CharField()
    background = serializers.CharField()


class StatSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    value = serializers.IntegerField()


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
    modificators = ModificatorSerializer(many=True, default=[])
    items = ItemSerializer(many=True, default=[])
    schools = SchoolSerializer(many=True, default=[])
    spells = SpellSerializer(many=True, default=[])


class CharacterTemplateValidationSerializer(serializers.Serializer):
    max_stats_points_count = serializers.IntegerField()
    max_modificators_count = serializers.IntegerField()
    max_items_count = serializers.IntegerField()
    max_spells_count = serializers.IntegerField()
    max_rank_grade = serializers.IntegerField()
    max_schools_count = serializers.IntegerField()


class CharacterTemplateFullSerializer(serializers.Serializer):
    data = CharacterTemplateSerializer()
    validation = CharacterTemplateValidationSerializer()


class CharacterBioDraftSerializer(serializers.Serializer):
    age = serializers.IntegerField(min_value=18, max_value=900)
    gender = serializers.ChoiceField(choices=GenderEnum.choices())
    appearance = serializers.CharField(allow_blank=True)
    background = serializers.CharField(allow_blank=True)


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
