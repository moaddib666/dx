from rest_framework import serializers

from apps.core.models import ImpactType, ImpactViolationType, AttributeType, CharacterStats, SkillTypes, EffectType


class StatRequirementSerializer(serializers.Serializer):
    """Serializer for StatRequirement DTO."""
    stat = serializers.ChoiceField(choices=CharacterStats.choices())
    value = serializers.IntegerField()


class ScalingSerializer(serializers.Serializer):
    """Serializer for Scaling DTO."""
    stat = serializers.CharField()
    value = serializers.FloatField()


class FormulaSerializer(serializers.Serializer):
    """Serializer for Formula DTO."""
    base = serializers.IntegerField()
    requires = StatRequirementSerializer(many=True)
    scaling = ScalingSerializer(many=True)
    max_efficiency = serializers.FloatField(required=False, allow_null=True)
    min_efficiency = serializers.FloatField(required=False, allow_null=True)


class ImpactSerializer(serializers.Serializer):
    """Serializer for Impact DTO."""
    kind = serializers.ChoiceField(choices=ImpactType.choices())
    type = serializers.ChoiceField(choices=ImpactViolationType.choices())
    formula = FormulaSerializer()


class SkillCostSerializer(serializers.Serializer):
    """Serializer for Cost DTO."""
    kind = serializers.ChoiceField(choices=AttributeType.choices())
    value = serializers.IntegerField()


class ModifierSerializer(serializers.Serializer):
    """Serializer for Modifier DTO."""
    label = serializers.CharField()
    formula = FormulaSerializer()


class EffectSerializer(serializers.Serializer):
    """Serializer for AssignableEffect DTO."""
    name = serializers.ChoiceField(choices=EffectType.choices())
    impact = ImpactSerializer(required=False, allow_null=True)
    base_chance = serializers.FloatField()
    duration_modifier = ModifierSerializer()
    stat_modifiers = ModifierSerializer(many=True)


class BaseSkillSerializer(serializers.Serializer):
    """Serializer for BaseSkill DTO."""
    name = serializers.CharField()
    description = serializers.CharField()
    school = serializers.UUIDField()
    multi_target = serializers.BooleanField()
    type = serializers.ChoiceField(choices=SkillTypes.choices())
    grade = serializers.IntegerField()
    cost = SkillCostSerializer(many=True)
    effect = EffectSerializer(many=True)
    impact = ImpactSerializer(many=True)
