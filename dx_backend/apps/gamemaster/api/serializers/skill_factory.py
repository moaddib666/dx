import uuid

from rest_framework import serializers
from apps.core.models import (
    ImpactType, ImpactViolationType, AttributeType, CharacterStats,
    SkillTypes, EffectType
)


class StatRequirementSerializer(serializers.Serializer):
    """Serializer for stat requirements in formulas."""
    stat = serializers.ChoiceField(choices=CharacterStats.choices())
    value = serializers.IntegerField(min_value=0)


class ScalingSerializer(serializers.Serializer):
    """Serializer for scaling values in formulas."""
    stat = serializers.CharField(max_length=100)
    value = serializers.FloatField()


class FormulaSerializer(serializers.Serializer):
    """Serializer for formula calculations."""
    base = serializers.IntegerField(min_value=0)
    requires = StatRequirementSerializer(many=True, required=False, default=list)
    scaling = ScalingSerializer(many=True, required=False, default=list)
    max_efficiency = serializers.FloatField(required=False, allow_null=True, default=None)
    min_efficiency = serializers.FloatField(required=False, allow_null=True, default=None)


class ImpactSerializer(serializers.Serializer):
    """Serializer for skill impacts."""
    kind = serializers.ChoiceField(choices=ImpactType.choices())
    type = serializers.ChoiceField(choices=ImpactViolationType.choices())
    formula = FormulaSerializer()


class CostSerializer(serializers.Serializer):
    """Serializer for skill costs."""
    kind = serializers.ChoiceField(choices=AttributeType.choices())
    value = serializers.IntegerField(min_value=0)


class ModifierSerializer(serializers.Serializer):
    """Serializer for effect modifiers."""
    label = serializers.CharField(max_length=200)
    formula = FormulaSerializer()


class AssignableEffectSerializer(serializers.Serializer):
    """Serializer for assignable effects."""
    name = serializers.ChoiceField(choices=EffectType.choices())
    impact = ImpactSerializer(required=False, allow_null=True)
    base_chance = serializers.FloatField(min_value=0.0, max_value=1.0)
    duration_modifier = ModifierSerializer()
    stat_modifiers = ModifierSerializer(many=True, required=False, default=list)


class SkillCreateSerializer(serializers.Serializer):
    """
    Serializer for creating a new skill.
    This serializer validates the input data for creating a skill with all nested structures.
    """
    name = serializers.CharField(max_length=200)
    description = serializers.CharField()
    school = serializers.UUIDField(required=False)
    multi_target = serializers.BooleanField(default=False)
    type = serializers.ChoiceField(choices=SkillTypes.choices())
    grade = serializers.IntegerField(min_value=1, max_value=10)
    cost = CostSerializer(many=True, required=False, default=list)
    effect = AssignableEffectSerializer(many=True, required=False, default=list)
    impact = ImpactSerializer(many=True, required=False, default=list)
